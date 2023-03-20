// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Rental Invoice', {
	refresh(frm){
		if(frm.doc.docstatus==1){
			add_purchase_invoice(frm)
		}
    },
	validate(frm){
		var supplier_currency = frm.doc.currency
        // frm.set_currency_labels(["tax_amount","grand_total"],customer_currency)
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], supplier_currency, "items");
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

});


frappe.ui.form.on('Subrent Timesheet', {

	rate(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"amount",child.rate*child.qty)	
	},
	qty(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"amount",child.rate*child.qty)	
	},
	price_list(frm,cdt,cdn){
        let rate = 0
		var child = locals[cdt][cdn];
        frappe.call({
            method: 'oil_and_gas_international.overriding.get_subrental_settings',
            args: {},
            callback: function(r) {
               console.log(r.message.redress)
                if (child.price_list == r.message.operationel){
                    rate = child.operational_running
                }
                else if (child.price_list == r.message.standby){
                    rate = child.standby
                }
                else if (child.price_list == r.message.post_rental_inspection_charges){
                    rate = child.post_rental_inspection_charges
                }
                else if  (child.price_list == r.message.lihdbr){
                    rate = child.lihdbr
                }
                else if (child.price_list == r.message.redress){
                    rate = child.redress
                }
                else {
                    rate = child.straight
                }
                frappe.model.set_value(cdt,cdn,"rate", rate)

            }
        });
            


            }

});


const add_purchase_invoice = () => {
	cur_frm.add_custom_button('Purchase Invoice', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Purchase Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_order", doc.sub_rental_order)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_timesheet", doc.sub_rental_timesheet)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_invoice", doc.name)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.supplier = doc.supplier
				cur_doc.conversion_rate = doc.conversion_rate
				cur_doc.is_sub_rent = 1
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
						expense_account:row.expense_head
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