// Copyright (c) 2016, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rental Report"] = {
	"filters": [
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options":'Item Group',
			"width": "80",
		},
		{
			"fieldname":"sub_group",
			"label": __("Sub Item Group"),
			"fieldtype": "Data",
			"width": "80",
		},
		{
			"fieldname":"child_group",
			"label": __("Child Group"),
			"fieldtype": "Data",
			"width": "80",
		},
	]
};
