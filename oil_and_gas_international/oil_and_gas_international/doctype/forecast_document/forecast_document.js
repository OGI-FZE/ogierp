// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Forecast Document', {
	refresh: function(frm) {
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "january","february","march","april","may","june","july","august","september","october","november","december"
        	], company_currency, "forecast_target");
	}
});
