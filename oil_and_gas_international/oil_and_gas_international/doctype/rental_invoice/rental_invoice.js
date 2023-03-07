// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Invoice', {

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