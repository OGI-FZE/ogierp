# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
			{
				"label": "Item code",
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options":'Item',
				"width": 170
			},
			{
				"label": "Item name",
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 170
			}
		]

	if filters.get("with_cust"):
		columns += [
			{
				"label": "",
				"fieldname": "status",
				"fieldtype": "Data",
				"width": 210
			},
			{
				"label": "Nos",
				"fieldname": "nos",
				"fieldtype": "Int",
				"width": 130
			},
		]
	else:
		columns += [
			{
				"label": "Available",
				"fieldname": "assets_available_for_rent",
				"fieldtype": "Int",
				"width": 130
			},
			{
				"label": "In Use",
				"fieldname": "assets_in_use",
				"fieldtype": "Int",
				"width": 130
			},
			{
				"label": "Total assets",
				"fieldname": "total_assets",
				"fieldtype": "Int",
				"width": 130
			},
		]
	return columns

def get_data(filters):
	if filters.get('item_code') : 
		if filters.get('exclude_zero'):
			all_asset_items = frappe.db.get_list('Item',
			    filters={
			        'name': filters.get('item_code'),
			        'is_string':1,
			        'total_assets':[">",0],
			    },
			    fields=['name','item_code' ,'item_name', 'total_assets', 'assets_in_use', 'assets_available_for_rent','usage_status'
			    ]
			)
		else:
			all_asset_items = frappe.db.get_list('Item',
			    filters={
			        'name': filters.get('item_code'),
			        'is_string':1
			    },
			    fields=['name','item_code' ,'item_name', 'total_assets', 'assets_in_use', 'assets_available_for_rent','usage_status'
			    ]
			)
	else:
		if filters.get('exclude_zero'):
			all_asset_items = frappe.db.get_list('Item',
			    filters={
			        'is_string':1,
			        'total_assets':[">",0],
			    },
			    fields=['name','item_code' ,'item_name', 'total_assets', 'assets_in_use', 'assets_available_for_rent','usage_status'
			    ]
			)
		else:
			all_asset_items = frappe.db.get_list('Item',
				filters={
			        'is_string':1
			    },
			    fields=['name','item_code' ,'item_name' , 'total_assets', 'assets_in_use', 'assets_available_for_rent','usage_status'
			    ]
			)
	if filters.get("with_cust"):
		# item code,item name,status,nos
		data = []
		for itm in all_asset_items:
			row = {
				'item_code':itm.item_code,
				'item_name':itm.item_name,
				'status':'Available',
				'nos':itm.assets_available_for_rent,
				'parent':'',
				'indent': 0.0
			}
			data.append(row)
			row = {
				'status':'In Use',
				'nos':itm.assets_in_use,
				'parent':'',
				'indent': 0.0
			}
			data.append(row)
			if itm.assets_in_use > 0:
				item_doc = frappe.get_doc("Item",itm.name)
				for line in item_doc.usage_status:
					if line.qty>0:
						row = {
							'status':line.customer,
							'nos':line.qty,
							'parent':'In Use',
							'indent': 1.0
						}
						data.append(row)

			row = {
				'status':'Total',
				'nos':itm.total_assets,
				'parent':''
			}
			data.append(row)
		print("data\n\n",data)
		return data
	else:
		return all_asset_items