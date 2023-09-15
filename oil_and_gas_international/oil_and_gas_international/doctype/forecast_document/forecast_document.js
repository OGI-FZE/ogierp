// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Forecast Document', {
	refresh: function(frm) {
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "january","february","march","april","may","june","july","august","september","october","november","december"
        	], company_currency, "forecast_target");

		// frm.set_df_property("forecast_target", "read_only", frm.is_new() ? 0 : 1);
		frm.set_df_property("fiscal_year", "read_only", frm.is_new() ? 0 : 1);
		frm.set_df_property("company", "read_only", frm.is_new() ? 0 : 1);
	},
	// before_save: function(frm) {
	// 	frm.set_value("version",frm.doc.version+1)
	// }
});

frappe.ui.form.on('Forecast target', {
	type: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		frappe.model.set_value(row.doctype, row.name, "customer", "")
		frappe.model.set_value(row.doctype, row.name, "customer_name", "")
		set_party(frm,row)
	},
	customer: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		set_party(frm,row)
	}
})

var set_party = function(frm, row){
	if (row.type == "Customer" && row.customer){
		frappe.db.get_value(row.type, row.customer, 'customer_name')
		.then(r => {
			if(r.message.customer_name){
				frappe.model.set_value(row.doctype, row.name, "customer_name", r.message.customer_name)
			}
		})
	}
	if (row.type == "Lead" && row.customer){
		frappe.db.get_value("Lead", row.customer, 'lead_name')
		.then(r => {
			if(r.message.lead_name){
				frappe.model.set_value(row.doctype, row.name, "customer_name", r.message.lead_name)
			}
		})
	}
}