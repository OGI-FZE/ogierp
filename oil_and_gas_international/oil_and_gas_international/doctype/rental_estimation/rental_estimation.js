// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt
var conv_rate = [1]
frappe.ui.form.on('Rental Estimation', {
	setup(frm) {
		set_query(frm)
	},
	refresh(frm) {
		create_custom_buttons()
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "base_operational_running","base_lihdbr","base_post_rental_inspection_charges","base_standby","base_straight","base_redress"
        	], company_currency, "items");
		var customer_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], customer_currency, "items");
	},
	onload(frm){
		if(frm.doc.customer && frm.doc.__islocal){
			frappe.db.get_value("Customer", {"name": frm.doc.customer}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
		// currency_change(frm, dt, dn)
      	convert_rate(frm)
	},
	customer(frm){
		if(frm.doc.customer){
			frappe.db.get_value("Customer", {"name": frm.doc.customer}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
	},
	currency(frm){
		get_conversion_rate(frm)
		var customer_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], customer_currency, "items");
		// convert_rates(frm)

	},
	conversion_rate(frm, dt, dn){
	    convert_rate(frm)
	},
  	validate(frm){
  		convert_rate(frm)
  	}
})

// const currency_change = function(frm, dt, dn){
//   frappe.model.get_value("Customer",frm.doc.customer_name || frm.doc.party_name, "default_currency",
//   function(d){
//     if(d.default_currency){
//       frappe.model.set_value(dt, dn, "currency",d.default_currency)
//     }
//   }
//   )
// }
const convert_rate = function(frm){
  if(frm.doc.items && frm.doc.docstatus!=1){
    conv_rate.push(frm.doc.conversion_rate)
      for(let row of frm.doc.items){
        var converted_op_rate = (row.base_operational_running)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'operational_running',converted_op_rate)
        var converted_lihdbr_rate = (row.base_lihdbr)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'lihdbr',converted_lihdbr_rate)
        var converted_pr_rate = (row.base_post_rental_inspection_charges)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'post_rental_inspection_charges',converted_pr_rate)
        var converted_standby_rate = (row.base_standby)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'standby',converted_standby_rate)
        var converted_straight_rate = (row.base_straight)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'straight',converted_straight_rate)
        var converted_redress_rate = (row.base_redress)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'redress',converted_redress_rate)
      }
  }
}

frappe.ui.form.on('Rental Estimation Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
		convert_rate(frm)
	},
})

const get_conversion_rate = (frm) => {
	let company_currency = erpnext.get_currency(frm.doc.company);
	// if (frm.doc.currency != company_currency) {
	frappe.call({
		method: "erpnext.setup.utils.get_exchange_rate",
		args: {
			from_currency: company_currency,
			to_currency: frm.doc.currency
		},
		callback: function(r) {
			if (r.message) {
				frm.set_value("conversion_rate",r.message)
			}
		}
	});
	// } else {
	// 	frm.set_value("conversion_rate",1)
	// }
	console.log("conv rate",frm.doc.conversion_rate)
}

// const convert_rates = (frm) => {
// 	console.log("not equal")
// 	frm.doc.items.forEach(item => {
// 		console.log("llll",item.item_code,item.base_operational_running,frm.doc.conversion_rate)
// 		frappe.model.set_value(item.doctype, item.name, 'operational_running', (item.base_operational_running * frm.doc.conversion_rate));
// 	})
// }

// Rental Estimation
const set_query = (frm) => {
	frm.fields_dict['items'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
		return {
			filters: [
				['item_type', '=', 'Rental']
			]
		}
	}
}

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0) {
		get_items_from_opportunity()
	} else if (status == 1) {
		add_rental_quotation()
	}
}

const get_items_from_opportunity = () => {
	const doctype = "Opportunity"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: {
				party_name: cur_frm.doc.customer,
			},
			date_field: "transaction_date",
			get_query() {
				return {
					filters: {
						opportunity_from: "Customer",
					}
				}
			},
			action(selections) {
				if (selections.length > 1) {
					frappe.msgprint(`Please select only single ${doctype} for importing items.`)
					return
				}
				cur_frm.call({
					method: "get_opportunity_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						cur_frm.doc.customer = data.party_name
						cur_frm.doc.opportunity = data.name
						cur_frm.doc.items = []

						for (const row of data.opportunity_items) {
							if (row.item_type == 'Rental') {
								const new_row = cur_frm.add_child("items", {
									qty: row.qty
								})
								const cdt = new_row.doctype
								const cdn = new_row.name
								frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
							}
						}

						cur_frm.refresh()
						cur_dialog.hide()
					}
				})

			}
		});
	}, 'Get Items From')
}

const add_rental_quotation = () => {
	cur_frm.add_custom_button('Rental Quotation', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Quotation'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.date = doc.date
				cur_doc.valid_till = doc.valid_till
				cur_doc.rate_type = doc.rate_type
				cur_doc.rental_estimation = doc.name

				cur_doc.items = []
				for (const row of doc.items) {
					const new_row = cur_frm.add_child('items', {
						'qty': row.qty,
						'estimate_rate': row.estimate_rate,
						'asset_location': row.asset_location,
						'rental_estimate': doc.name,
						'rental_estimate_item': row.name,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

// Rental Estimation Item
const calculate_lost_and_damage_price = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	const item_code = row.item_code

	frappe.call({
		method: "oil_and_gas_international.events.shared.get_lost_and_damage_prices",
		args: {
			item_code
		},
		callback(r) {
			const data = r.message
			row.operational_running = data[0]
			row.standby = data[1]
			row.lihdbr = data[2]
			row.redress = data[3]
			row.straight = data[4]
			row.post_rental_inspection_charges = data[5]
			row.base_operational_running = data[0]
			row.base_standby = data[1]
			row.base_lihdbr = data[2]
			row.base_redress = data[3]
			row.base_straight = data[4]
			row.base_post_rental_inspection_charges = data[5]
			frm.refresh()
		}
	})
}