frappe.listview_settings['Rental Order'] = {
	add_fields: ["status", "customer", "division", "date"],
	get_indicator: function (doc) {
		if (doc.status === "Completed") {
			// Closed
			return [__("Completed"), "green", "status,=,Completed"];
		} else if (doc.status === "On Rent") {
			// on hold
			return [__("On Rent"), "orange", "status,=,On Rent"];
		} 
	},
};
