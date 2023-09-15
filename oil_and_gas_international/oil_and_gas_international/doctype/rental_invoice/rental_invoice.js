// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Invoice', {

	setup(frm){
		frm.set_query("taxes_and_charges", function() {
			return {
				filters: {
                    "company":frm.doc.company
				}
			};
		});
	},
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

	payment_term(frm){
		if (!frm.doc.payment_term){
			frm.doc.taxes = []
			frm.refresh_field('payment_term')
		}
		frappe.call({
            method: 'oil_and_gas_international.overriding.get_payment',
            args: {
                p: frm.doc.payment_term,
            },
            callback: function(r) {
				console.log(r.message)
				frm.add_child("payment_schedule",{
					"payment_term": r.message[0]['payment_term'],
					"description": r.message[0]['description'],
					"due_date": frm.doc.delivery_date,
					"invoice_portion":r.message[0]['invoice_portion'],
					"discount_type":r.message[0]['discount_type'],
					"discount":r.message[0]['discount'],
					"payment_amount": frm.doc.grand_total,
				})
				frm.refresh_field('payment_schedule')
            }
        })

	},

	taxes_and_charges(frm){
		if (!frm.doc.taxes_and_charges){
			frm.doc.taxes = []
			var discount = 0
			if (!frm.doc.additional_discount_percentage){
				var discount = frm.doc.total*0/100
			}
			else{
				discount = frm.doc.total*frm.doc.additional_discount_percentage/100
			}
			frm.set_value("grand_total",frm.doc.total-discount)
			frm.refresh_field('taxes')

		}
		frappe.call({
            method: 'oil_and_gas_international.overriding.getTax',
            args: {
                tx: frm.doc.taxes_and_charges,
            },
            callback: function(r) {
				frm.clear_table("taxes")
				frm.add_child("taxes",{
					"charge_type": r.message[0]["charge_type"],
					"account_head": r.message[0]["account_head"],
					"rate": r.message[0]["rate"],
					"tax_amount": (frm.doc.total*r.message[0]['rate'])/100,
					"total": (frm.doc.total + (frm.doc.total*r.message[0]['rate'])/100),
					"description": r.message[0]["description"]				
				})
				var gt = (frm.doc.total + (frm.doc.total*r.message[0]['rate'])/100)
				var discount = 0
				if (!frm.doc.additional_discount_percentage){
					var discount = gt*0/100
				}
				else{
					discount = gt*frm.doc.additional_discount_percentage/100
				}
				console.log(discount)
				console.log(gt)
				frm.set_value("grand_total",gt-discount)
				frm.refresh_field('taxes')
                        }
        })
		
     },

	additional_discount_percentage(frm){
		var discount = frm.doc.additional_discount_percentage*frm.doc.grand_total/100
		frm.set_value('discount_amount',discount)
		frm.set_value("grand_total",frm.doc.grand_total-discount)
		if (frm.doc.additional_discount_percentage == 0){
			if (frm.doc.taxes_and_charges){
				frm.set_value('grand_total',frm.doc.taxes[0].total)
			}
			else {
				frm.set_value('grand_total',frm.doc.total)
			}
		}
	

    },

	// discount_amount(frm){
	// 	var discount_per = (frm.doc.discount_amount/frm.doc.grand_total)*100
	// 	console.log(discount_per)
	// 	frm.set_value('additional_discount_percentage',discount_per)
	// 	frm.set_value("grand_total",frm.doc.grand_total-frm.doc.discount_amount)
    // },
			

	delivery_date(frm){
		for (const row of frm.doc.items){
			frappe.model.set_value(row.doctype,row.name,"delivery_date",frm.doc.delivery_date)
		}
	},

	selling_price_list(frm){
		let rate = 0
		for (const row of frm.doc.items){
			
			if (frm.doc.selling_price_list == "Operational/Running"){
				rate = row.operational_running
			}
			else if (frm.doc.selling_price_list == "Standby"){
				rate = row.standby
			}
			else if (frm.doc.selling_price_list == "Post Rental Inspection charges"){
				rate = row.post_rental_inspection_charges
			}
			else if  (frm.doc.selling_price_list == "LIH/DBR"){
				rate = row.lihdbr
			}
			else if (frm.doc.selling_price_list == "Redress"){
				rate = row.redress
			}
			else {
				rate = row.straight
			}
			const cdt = row.doctype
			const cdn = row.name
			frappe.model.set_value(cdt,cdn,"rate", rate)

		}

				
				
	}

});


frappe.ui.form.on('Proforma Invoice Item', {

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
				cur_doc.additional_discount_percentage = doc.additional_discount_percentage
				cur_doc.discount_amount = doc.discount_amount
				cur_doc.rental_timesheet = doc.rental_timesheet
				cur_doc.customer_address = doc.customer_address
				cur_doc.contact_person = doc.customer_contact
				cur_doc.payment_terms_template = doc.payment_term
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "taxes_and_charges", doc.taxes_and_charges)
				// cur_doc.ignore_pricing_rule = 1
				cur_doc.items = []
				// for (const row of doc.payment_schedule){
				// 	const new_row = cur_frm.add_child("payment_schedule",{
				// 		"payment_term": row.payment_term,
				// 		"description": row.description,
				// 		"due_date": row.due_date,
				// 		"invoice_portion":row.invoice_portion,
				// 		"discount_type":row.discount_type,
				// 		"discount":row.discount,
				// 		"payment_amount": row.amount,
				// 	})
				// }
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