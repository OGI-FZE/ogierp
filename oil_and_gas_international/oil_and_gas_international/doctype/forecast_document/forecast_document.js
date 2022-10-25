// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Forecast Document', {
	refresh: function(frm) {
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "january","february","march","april","may","june","july","august","september","october","november","december"
        	], company_currency, "forecast_target");

		frm.set_df_property("forecast_target", "read_only", frm.is_new() ? 0 : 1);
		frm.set_df_property("fiscal_year", "read_only", frm.is_new() ? 0 : 1);
		frm.set_df_property("company", "read_only", frm.is_new() ? 0 : 1);
	},
	before_save: function(frm) {
		frm.set_value("version",frm.doc.version+1)
	}
});
