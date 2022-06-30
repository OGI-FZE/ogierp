# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff,today
from datetime import date

def execute(filters=None):
	columns = [
		{	
			"label": "Asset",
			"fieldtype": "Link",
			"options":"Asset",
			"fieldname": "asset",
			"width": 120
		},
		{
			"label": "Asset Name",
			"fieldtype": "Data",
			"fieldname": "asset_name",
			"width": 150
		},
		{
			"label": "Life",
			"fieldtype": "Int",
			"fieldname": "life",
			"width": 80
		},
		{
			"label": "Operational/Running",
			"fieldtype": "Int",
			"fieldname": "op",
			"width": 120
		},
		{
			"label": "Standby",
			"fieldtype": "Int",
			"fieldname": "standby",
			"width": 100
		},
		{
			"label": "Straight",
			"fieldtype": "Int",
			"fieldname": "straight",
			"width": 100
		},
		{
			"label": "Utilization",
			"fieldtype": "Int",
			"fieldname": "utilization",
			"width": 100
		},
		{
			"label": "Revenue",
			"fieldtype": "Float",
			"fieldname": "revenue",
			"width": 80
		},
		{
			"label": "Supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"fieldname": "supplier",
			"width": 170
		},
		{
			"label": "Purchase Date",
			"fieldtype": "Date",
			"fieldname": "pur_date",
			"width": 100,
		},
		{
			"label": "Gross Purchase Rate",
			"fieldtype": "Float",
			"fieldname": "gross_rate",
			"width": 100,
		},
	]
	data = get_data(filters)
	return columns, data

def get_data_from_timesheets(filters):
	all_list = frappe.get_list('Rental Timesheet', filters = {'start_date':['>=', filters.from_date], 'end_date':['<=', filters.to_date]})
	final_dict = frappe._dict()
	for i in all_list:
		try:
			take_one = frappe.get_doc('Rental Timesheet' , i['name'])
			take_one_list = take_one.items
			for j in take_one_list:
				base_1 = ''
				days_1 = ''
				assets = (j.assets).split('\n')
				assets.remove('')
				if j.operational_running_check:
					type = "op"
					base_1 = j.base_operational_running
					days_1 = j.operational_running_days
				elif j.standby_check:
					type="standby"
					base_1 = j.base_standby
					days_1 = j.standby_days
				else:
					type = "straight"
					base_1 = j.base_straight
					days_1 = j.straight_days
				for k in assets:
					try:
						if final_dict[k]:
							final_dict[k][type] += base_1 * days_1
							final_dict[k].utilization += days_1
							final_dict[k].revenue += base_1 * days_1
					except:
						new_asset = frappe._dict(asset = k, op = 0, standby = 0, straight = 0, utilization = 0, revenue = 0)
						new_asset[type] += base_1 * days_1
						new_asset.utilization += days_1
						new_asset.revenue += base_1 * days_1
						#asset details
						[asset_name, life, pur_date, supplier, gross_rate, asset_category] = get_asset_details(k)
						new_asset.setdefault("asset_name", asset_name)
						new_asset.setdefault("life", life)
						new_asset.setdefault("pur_date", pur_date)
						new_asset.setdefault("supplier", supplier)
						new_asset.setdefault("gross_rate", gross_rate)
						new_asset.setdefault("asset_category", asset_category)
						final_dict[k] = new_asset
		except:
			pass
	return final_dict

def get_asset_details(asset):
	details = frappe.get_doc("Asset", asset)
	purchase_date = details.purchase_date
	current_date = date.today()
	delta = current_date - purchase_date
	return details.asset_name, delta.days, purchase_date, details.supplier_info, details.gross_purchase_amount, details.asset_category

def get_data(filters):
	data = []
	all_data = get_data_from_timesheets(filters)
	data_list = list(all_data.values())
	if(filters.asset_category):
		filtered_data = [d for d in data_list if d['asset_category'] == filters.asset_category]
		if(filters.asset):
			try:
				data = list(filter(lambda x: x['asset'] == filters.asset, filtered_data))
				return data
			except:
				return []
		data = filtered_data
	return data

