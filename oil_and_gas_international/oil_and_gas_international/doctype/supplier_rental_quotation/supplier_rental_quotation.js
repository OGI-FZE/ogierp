// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

var conv_rate = [1]
frappe.ui.form.on('Supplier Rental Quotation', {
	setup: function (frm) {
		frm.set_query("item_code", "items", function(doc, cdt, cdn) {
			return {
				filters: {
					is_fixed_asset: 1,
				}
			}
		})
	},
	refresh(frm) {
		create_custom_buttons(frm)
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "base_operational_running","base_lihdbr","base_post_rental_inspection_charges","base_standby","base_straight","base_redress"
        	], company_currency, "items");
		var billing_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], billing_currency, "items");
	},
	onload(frm){
		if(frm.doc.supplier && frm.doc.__islocal){
			frappe.db.get_value("Supplier", {"name": frm.doc.supplier}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
      	convert_rate(frm)
	},
	supplier(frm){
		if(frm.doc.supplier){
			frappe.db.get_value("Supplier", {"name": frm.doc.supplier}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
	},
	currency(frm){
		get_conversion_rate(frm)
		var billing_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], billing_currency, "items");

	},
	conversion_rate(frm){
    	convert_rate(frm)
  	},
  	validate(frm){
  		convert_rate(frm)
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

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 1) {
		add_supplier_rental_order()
	}
}

const add_supplier_rental_order = () => {
	cur_frm.add_custom_button('Supplier Rental Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.supplier = doc.supplier
				cur_doc.supplier_rental_quotation = doc.name
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate

				// frappe.model.set_value('Supplier Rental Order', cur_doc.name, "currency", doc.currency)
				// frappe.model.set_value('Supplier Rental Order', cur_doc.name, "conversion_rate", doc.conversion_rate)
				

				cur_doc.items = []
				for (const row of doc.items) {
					let rate = row.rate
					if (doc.rate_type == "Per Month") {
						rate = rate / 30
					}

					const new_row = cur_frm.add_child('items', {
						'rate': rate,
						'asset_location': row.asset_location,
						'supplier_rental_quotation': doc.name,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
					setTimeout(function() {
						frappe.model.set_value(cdt, cdn, "qty", row.qty)
						frappe.model.set_value(cdt, cdn, "operational_running", row.operational_running)
						frappe.model.set_value(cdt, cdn, "lihdbr", row.lihdbr)
						frappe.model.set_value(cdt, cdn, "standby", row.standby)
						frappe.model.set_value(cdt, cdn, "redress", row.redress)
						frappe.model.set_value(cdt, cdn, "straight", row.straight)
						frappe.model.set_value(cdt, cdn, "base_operational_running", row.base_operational_running)
						frappe.model.set_value(cdt, cdn, "base_lihdbr", row.base_lihdbr)
						frappe.model.set_value(cdt, cdn, "base_standby", row.base_standby)
						frappe.model.set_value(cdt, cdn, "base_redress", row.base_redress)
						frappe.model.set_value(cdt, cdn, "base_straight", row.base_straight)
						frappe.model.set_value(cdt, cdn, "base_post_rental_inspection_charges", row.base_post_rental_inspection_charges)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}



frappe.ui.form.on('Supplier Rental Quotation Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},
	qty(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	rate(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	amount(frm) {
		calc_total_amount(frm)
	},
});

const calc_total_amount = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.amount) total += row.amount
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total', total)
}

// Supplier Rental Quotation Item
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


const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate)
}
