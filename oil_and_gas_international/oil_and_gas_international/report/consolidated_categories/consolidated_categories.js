// Copyright (c) 2016, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consolidated Categories"] = {
	"filters": [
		{
			"fieldname":"item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options":"Item",
			"width": 100,
		},
		{
			"fieldname":"child_group",
			"label": __("Child Group"),
			"fieldtype": "Link",
			"options":'Item Group',
			"width": "80",
		},
	]
};
