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
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options":'Item Group',
			"width": "80",
		},
	]
};
