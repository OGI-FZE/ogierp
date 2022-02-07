// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rental Asset Report"] = {
	"filters": [
		// {
		// 	"fieldname":"item_code",
		// 	"label": __("Item Code"),
		// 	"fieldtype": "Link",
		// 	"options":"Item",
		// 	"width": 100,
		// },
		{
			"fieldname":"asset",
			"label": __("Asset"),
			"fieldtype": "Link",
			"options":"Asset",
			"width": 100,
		},
		{
			"fieldname":"grand_parent_group",
			"label": __("Category"),
			"fieldtype": "Link",
			"options":'Item Group',
			"width": "80",
		},
		{
			"fieldname":"parent_group",
			"label": __("Sub Category"),
			"fieldtype": "Link",
			"options":'Item Group',
			"width": "80",
		},
		{
			"fieldname":"child_group",
			"label": __("Child Category"),
			"fieldtype": "Link",
			"options":'Item Group',
			"width": "80",
		},

	]
};
