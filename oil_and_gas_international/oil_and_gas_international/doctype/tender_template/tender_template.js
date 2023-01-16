// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tender Template', {
	// refresh: function(frm) {

	// }
});



frappe.ui.form.on('Tender Template Activity', {
	activity: function(frm) {
		frm.doc.activities.forEach(function(act){
			frappe.db.get_value("Tender Activity", act.activity, "date", (r) => {
					console.log(act.date)
					frappe.model.set_value(act.doctype,act.name,"date", r.date)
			});

			frappe.db.get_value("Tender Activity", act.activity, "activity_type", (r) => {
				console.log(act.date)
				frappe.model.set_value(act.doctype,act.name,"activity_type", r.activity_type)
		    });

			frappe.db.get_value("Tender Activity", act.activity, "status", (r) => {
				console.log(act.date)
				frappe.model.set_value(act.doctype,act.name,"status", r.status)
		    });
		})
	 }
});
