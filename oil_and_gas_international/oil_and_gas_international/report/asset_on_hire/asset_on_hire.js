// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset on Hire"] = {
	"filters": [

		{
			"fieldname":"asset_code",
			"label": __("Asset Code"),
			"fieldtype": "Link",
			"options":"Asset",
			"width": 100,
		},

	]
};
