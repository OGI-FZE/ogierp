// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset Utilization Report"] = {
	"filters": [
		{
			"fieldname":"asset",
			"label": __("Asset"),
			"fieldtype": "Link",
			"options":"Asset",
			"width": 100,
			"reqd":1,
			on_change: () => {
				var asset = frappe.query_report.get_filter_value('asset');
				if(asset){
					frappe.db.get_value('Asset', asset, "asset_name", function(value) {
						frappe.query_report.set_filter_value('asset_name', value["asset_name"]);
					});
					frappe.db.get_value('Asset', asset, "purchase_date", function(value) {
						frappe.query_report.set_filter_value('pur_date', value["purchase_date"]);
					});
					frappe.db.get_value('Asset', asset, "purchase_receipt", function(value) {
						if(value['purchase_receipt']){
							frappe.db.get_value('Purchase Receipt', value['purchase_receipt'], "supplier", function(v){
								frappe.query_report.set_filter_value('supplier', v["supplier"]);
							});
						}
					});
				}
			}
		},
		{
			"label": "Description",
			"fieldtype": "Data",
			"fieldname": "asset_name",
			"width": 220,
			'read_only':1
		},
		{
			"label": "Purchase Date",
			"fieldtype": "Date",
			"fieldname": "pur_date",
			"width": 100,
			'read_only':1
		},
		{
			"label": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": 'Supplier',
			"width": 130,
			'read_only':1
		}
	]
};
