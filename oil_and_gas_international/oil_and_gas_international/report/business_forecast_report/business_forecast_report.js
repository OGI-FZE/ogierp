// Copyright (c) 2022, Craft Interactive LLC
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Business Forecast Report"] = {
	"filters": [
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company")
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: frappe.sys_defaults.fiscal_year
		},
		{
			fieldname:"customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: [
				{ "value": "Country", "label": __("Country") },
				{ "value": "SalesPerson", "label": __("Sales Person") },
			],
			default: "Country"
		},

	]
};
