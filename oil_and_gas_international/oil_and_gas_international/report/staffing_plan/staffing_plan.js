// Copyright (c) 2022, . and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Staffing Plan"] = {
	"filters": [
	{
		"fieldname": "company",
		"label": __("Company"),
		"fieldtype": "Link",
		"options": "Company",
		"reqd": 1,
		"default": frappe.defaults.get_user_default("company"),
	},

	{
		fieldname: "fiscal_year",
		label: __("Fiscal Year"),
		fieldtype: "Link",
		options: "Fiscal Year",
		default: frappe.defaults.get_user_default("fiscal_year"),
		reqd: 1,
		on_change: function (query_report) {
			var fiscal_year = query_report.get_values().fiscal_year;
			if (!fiscal_year) {
				return;
			}
			frappe.model.with_doc("Fiscal Year", fiscal_year, function (r) {
				var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
				frappe.query_report.set_filter_value({
					from_date: fy.year_start_date,
					to_date: fy.year_end_date
				});
			});
		}
	},


	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	}
};