// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset Utilization"] = {
	"filters": [
		{
			"fieldname":"asset_category",
			"label": __("Asset Category"),
			"fieldtype": "Link",
			"options":"Asset Category",
			"width": 100,
			"reqd":1,
		},
		{
			"fieldname":"asset",
			"label":__("Asset"),
			"fieldtype": "Link",
			"options": "Asset",
			"width":100,
			get_query: () => {
				var asset_category = frappe.query_report.get_filter_value('asset_category');
				return {
					filters: {
						'asset_category': asset_category
					}
				}
			}
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 100,
			"default":frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 100,
			"default":frappe.datetime.get_today()
		},
	]
};
