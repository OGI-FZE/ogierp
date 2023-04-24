// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt
frappe.ui.form.on('NCR', {
	setup: function (frm) {
		frm.set_query("ncr_against", function () {
		  return {
			"filters": {
			  "name": ["in", ["Customer", "Supplier", "Employee"]],
			}
		  }
		})
	}
});
