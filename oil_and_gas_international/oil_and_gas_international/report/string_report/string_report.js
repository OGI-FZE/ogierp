// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["String Report"] = {
	"filters": [
		{
			"fieldname":"item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options":"Item",
			"width": 100,
		},
		{
			"fieldname": "exclude_zero",
			"label": __("Exclude All Zero Entries"),
			"fieldtype": "Check",
			"default": 1
		},
		{
			"fieldname": "with_cust",
			"label": __("Show customer wise"),
			"fieldtype": "Check",
			"default": 1
		}

	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (!data.parent) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");

			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};
