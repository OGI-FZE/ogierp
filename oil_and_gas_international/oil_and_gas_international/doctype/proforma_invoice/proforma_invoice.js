// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Proforma Invoice', {
	refresh(frm){
		if(frm.doc.docstatus==1){
			add_sales_invoice(frm)
		}
    },
	validate(frm){
		var customer_currency = frm.doc.currency
        // frm.set_currency_labels(["tax_amount","grand_total"],customer_currency)
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], customer_currency, "items");
    },

	taxes_and_charges(frm){
		frappe.call({
            method: 'oil_and_gas_international.overriding.getTax',
            args: {
                tx: frm.doc.taxes_and_charges,
            },
            callback: function(r) {
				frm.add_child("taxes",{
					"charge_type": r.message[0]["charge_type"],
					"account_head": r.message[0]["account_head"],
					"rate": r.message[0]["rate"],
					"tax_amount": (frm.doc.total*r.message[0]['rate'])/100,
					"total": (frm.doc.total + (frm.doc.total*r.message[0]['rate'])/100),
					"description": r.message[0]["description"]
					


				})
				frm.refresh_field('taxes')
                        }
        })
     },
			

	delivery_date(frm){
		for (const row of frm.doc.items){
			frappe.model.set_value(row.doctype,row.name,"delivery_date",frm.doc.delivery_date)
		}
	},

	selling_price_list(frm){
		for (const row of frm.doc.items){
			const cdt = row.doctype
			const cdn = row.name
			frappe.call({
				method: "oil_and_gas_international.overriding.set_rate",
				args:{"item":row.item_code,
					  "price_list": frm.doc.selling_price_list},
	
				callback: function(r) {
					frappe.model.set_value(cdt,cdn,"rate",r.message)	
				}
			});
			
		}

				
				
	}

});


frappe.ui.form.on('Proforma Invoice Item', {
	item_code(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.call({
			method: "oil_and_gas_international.overriding.set_rate",
			args:{"item":child.item_code,
				  "price_list": frm.doc.selling_price_list},

			callback: function(r) {
				frappe.model.set_value(cdt,cdn,"rate",r.message)	
			}
		});
	},
	rate(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"amount",child.rate*child.qty)	
	},
	qty(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"amount",child.rate*child.qty)	
	}

});


const add_sales_invoice = () => {
	cur_frm.add_custom_button('Sales Invoice', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sales Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_invoice", doc.name)

				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.customer = doc.customer
				cur_doc.conversion_rate = doc.conversion_rate
				cur_doc.against_rental_order = 1
				cur_doc.department = doc.department
				cur_doc.division = doc.division
				cur_doc.rental_timesheet = doc.rental_timesheet
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "taxes_and_charges", doc.taxes_and_charges)
				// cur_doc.ignore_pricing_rule = 1
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						item_code:row.item_code,
						item_name:row.item_name,
						qty: row.qty,
						description:row.description,
						start_date:row.start_date_,
						end_date:row.end_date,
						rate:row.rate*row.days,
						days:row.days,
						uom:row.uom,
						income_account:row.income_account,
						expense_account:row.expense_account
					})
				
					const cdt = new_row.doctype
					const cdn = new_row.name

					// frappe.model.set_value(cdt, cdn, "rate", row.rate)
					// frappe.model.set_value(cdt, cdn, "item_name", row.item_name)
					// frappe.model.set_value(cdt, cdn, "description", row.description)

				}
				cur_frm.refresh()
				
			}
		])
	}, 'Create')
}