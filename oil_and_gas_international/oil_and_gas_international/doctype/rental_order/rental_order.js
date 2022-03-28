// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

var conv_rate = [1]
frappe.ui.form.on('Rental Order', {
	setup(frm) {
		set_query(frm)
	},

	refresh(frm) {
		create_custom_buttons(frm)
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "base_operational_running","base_lihdbr","base_post_rental_inspection_charges","base_standby","base_straight","base_redress","base_total_amount"
        	], company_currency, "items");
		var customer_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress","total_amount"
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
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress","total_amount"
        ], customer_currency, "items");

	},
	conversion_rate(frm){
    	convert_rate(frm)
  	},
  	validate(frm){
  		convert_rate(frm)
  	},
	taxes_and_charges(frm) {
		frappe.call({
			method: "oil_and_gas_international.oil_and_gas_international.doctype.rental_order.rental_order.get_taxes",
			args: {
				'ro':frm.doc.name,
				'tt':frm.doc.taxes_and_charges
			},
			callback(r) {
				let all_taxes = r.message
				all_taxes.forEach(tax => {
					let row = frm.add_child('taxes', {
						'charge_type': tax.charge_type,
						'account_head': tax.account_head,
						'description': tax.description,
						'rate': tax.rate,
					});
				});
				frm.refresh();
			}
		})
	}
});

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
        var converted_base_total_amount = (row.total_amount)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'base_total_amount',converted_base_total_amount)
      }
  }
}

const get_conversion_rate = (frm) => {
	let company_currency = erpnext.get_currency(frm.doc.company);
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
}

// Rental Order Item
frappe.ui.form.on('Rental Order Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},

	from_date(frm, cdt, cdn) {
		calc_days_of_rent(frm, cdt, cdn)
	},

	to_date(frm, cdt, cdn) {
		calc_days_of_rent(frm, cdt, cdn)
	},

	qty(frm, cdt, cdn) {
		calc_total_qty(frm, cdt, cdn)
	},
});

// Rental Order
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
		get_items_from_rental_quotation()
	} else if (status == 1) {
		add_project()
		add_rental_issue_note()
		add_rental_receipt()
		add_material_request()
		add_asset_formation()
		add_purchase_order()
		add_purchase_invoice()
		add_rental_timesheet()
	}
}


const get_items_from_rental_quotation = () => {
	const doctype = "Rental Quotation"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: { customer: cur_frm.doc.customer, },
			date_field: "date",
			get_query() {
				return {
					filters: {docstatus:1}
				}
			},
			action(selections) {
				if (selections.length > 1) {
					frappe.msgprint(`Please select only single ${doctype} for importing items.`)
					return
				}
				cur_frm.call({
					method: "get_rental_quotation_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						const cur_doc = cur_frm.doc
						cur_doc.customer = data.customer
						cur_doc.rental_quotation = data.name

						cur_doc.items = []
						for (const row of data.rq_items) {
							let rate = row.rate
							if (data.rate_type == "Per Month") {
								rate = rate / 30
							}

							const new_row = cur_frm.add_child('items', {
								'rate': rate,
								'asset_location': row.asset_location,
								'rental_estimation': row.rental_estimate,
								'rental_quotation': data.name,
							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
							frappe.model.set_value(cdt, cdn, "qty", row.qty)
						}

						cur_frm.refresh()
						cur_dialog.hide()
					}
				})
			}
		});
	}, 'Get Items From')
}

const add_project = () => {
	cur_frm.add_custom_button('Project', () => {
		const doc = cur_frm.doc
		// frm.clear_table('items');
		frappe.run_serially([
			() => frappe.new_doc('Project'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.project_name = doc.name
				cur_doc.expected_start_date = doc.date
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)
				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_rental_issue_note = () => {
	cur_frm.add_custom_button('Rental Issue Note', () => {
		const doc = cur_frm.doc
		// frm.clear_table('items');
		frappe.run_serially([
			() => frappe.new_doc('Rental Issue Note'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.departments = doc.departments
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)
				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_rental_receipt = () => {
	cur_frm.add_custom_button('Rental Receipt', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Receipt'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.departments = doc.departments
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)

				cur_frm.refresh()
			}
		])
	}, 'Create')
}
const add_rental_timesheet = () => {
	cur_frm.add_custom_button('Rental Timesheet', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Timesheet'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)

				cur_frm.refresh()
			}
		])
	}, 'Create')
}


const add_material_request = () => {
	const doctype = "Material Request"
	cur_frm.add_custom_button(doctype, () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc(doctype),
			() => {
				const cur_doc = cur_frm.doc
				const cdt = cur_doc.doctype
				const cdn = cur_doc.name

				frappe.model.set_value(cdt, cdn, "rental_order", doc.name)
				cur_frm.refresh()
			}
		])
	}, 'Create')
}


const add_asset_formation = () => {
	cur_frm.add_custom_button('Asset Formation', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Asset Formation'),
			() => {
				const cur_doc = cur_frm.doc
				const cdt = cur_doc.doctype
				const cdn = cur_doc.name

				cur_doc.rental_order = doc.name
				if (doc.items.length == 1)
					frappe.model.set_value(cdt, cdn, "asset_item_code", doc.items[0].item_code)


				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_purchase_order = () => {
	cur_frm.add_custom_button('Purchase Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Purchase Order'),
			() => {
				const cur_doc = cur_frm.doc
				// cur_doc.rental_order = doc.name
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: row.qty
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

const add_purchase_invoice = () => {
	cur_frm.add_custom_button('Purchase Invoice', () => {
		const rate=[]
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Purchase Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				// cur_doc.rental_order = doc.name
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: row.qty
					})
					rate.push(row.total_amount)
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
				}

				cur_frm.refresh()
				for(let row of cur_doc.items ){
					const cdt = row.doctype
					const cdn = row.name
					frappe.model.set_value(cdt, cdn, "rate", row.total_amount)
				}
			}
		])
	}, 'Create')
}

const calc_total_qty = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.qty) total += row.qty
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_qty', total)
}


// Rental Order Item

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




const calc_days_of_rent = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.from_date && row.to_date) {
		const to_date = new Date(row.to_date)
		const from_date = new Date(row.from_date)
		const difference = Math.floor((to_date - from_date) / (1000 * 60 * 60 * 24) + 1)

		if (difference < 1) {
			frappe.msgprint("To Date can't be before From date!")
			frappe.model.set_value(cdt, cdn, 'days_of_rent', 0)
			return
		}
		frappe.model.set_value(cdt, cdn, 'days_of_rent', difference)
	}
}