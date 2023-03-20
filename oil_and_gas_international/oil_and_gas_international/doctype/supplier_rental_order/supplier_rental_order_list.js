frappe.listview_settings['Supplier Rental Order'] = {
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
