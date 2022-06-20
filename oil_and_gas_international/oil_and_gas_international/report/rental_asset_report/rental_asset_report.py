# Copyright (c) 2022, Craft and contributors
# For license information, please see license.txt

from itertools import count
from typing import Counter

from numpy import take
import frappe
from frappe import _, get_all

# DONE by MR.index 0_0 A.M
def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": "Asset Id",
			"fieldname": "asset_id",
			"fieldtype": "Link",
			"options": 'Asset',
			"width": 130
		},
		{
			"label": "Asset Name",
			"fieldname": "asset_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": "Category",
			"fieldname": "asset_category",
			"fieldtype": "Link",
			"options":'Item Group',
			"width": 130
		},
		{
			"label": "location",
			"fieldname": "location",
			"fieldtype": "Link",
			"options":'Location',
			"width": 130
		},


		{
			"label": "Company",
			"fieldname": "company",
			"fieldtype": "Link",
			"options":'Company',
			"width": 130
		},
{
			"label": "Status",
			"fieldtype": "Data",
			"fieldname": "status",
			"width": 150
		},
		{
			"label": "Rental Status",
			"fieldtype": "Select",
			"fieldname": "rental_status",
			"width": 170
		},

			{
			"label": "Item name",
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 130
		},
			{
			"label": "Item code",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options":'Item',
			"width": 130
		},
			
		{
			"label": "Sub Category",
			"fieldname": "parent_group",
			"fieldtype": "Link",
			"options":'Item Group',
			"width": 130
		},
		{
			"label": "Sub-sub Category",
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options":'Item Group',
			"width": 130
		},
		

		{
			"label": "Type",
			"fieldtype": "Data",
			"fieldname": "type",
			"width": 170
		},
	
		{
			"label": "PPF",
			"fieldtype": "Data",
			"fieldname": "ppf",
			"width": 170
		},
	
	
		{
			"label": "tool joint id ",
			"fieldtype": "Data",
			"fieldname": "tool_joint_id",
			"width": 170
		},
	
	{
			"label": "tool joint od",
			"fieldtype": "Data",
			"fieldname": "tool_joint_od",
			"width": 170
		},
	{
			"label": "range",
			"fieldtype": "Data",
			"fieldname": "range",
			"width": 170
		},
	{
			"label": "od size",
			"fieldtype": "Data",
			"fieldname": "od_size_",
			"width": 170
		},
	{
			"label": "top connection",
			"fieldtype": "Data",
			"fieldname": "top_connection",
			"width": 170
		},
	{
			"label": "bottom connection",
			"fieldtype": "Data",
			"fieldname": "bottom_connection",
			"width": 170
		},
	{
			"label": "service",
			"fieldtype": "Data",
			"fieldname": "service",
			"width": 170
		},
	{
			"label": "make",
			"fieldtype": "Data",
			"fieldname": "make",
			"width": 170
		},
	{
			"label": "size",
			"fieldtype": "Data",
			"fieldname": "size",
			"width": 170
		},
	{
			"label": "pin connection",
			"fieldtype": "Data",
			"fieldname": "pin_connection",
			"width": 170
		},
	{
			"label": "box connection",
			"fieldtype": "Data",
			"fieldname": "box_connection",
			"width": 170
		},
	{
			"label": "od",
			"fieldtype": "Data",
			"fieldname": "od",
			"width": 170
		},
	{
			"label": "wrap angle",
			"fieldtype": "Data",
			"fieldname": "wrap_angle",
			"width": 170
		},
	{
			"label": "hard facing",
			"fieldtype": "Data",
			"fieldname": "hard_facing",
			"width": 170
		},
	{
			"label": "model",
			"fieldtype": "Data",
			"fieldname": "model",
			"width": 170
		},
	{
			"label": "degree",
			"fieldtype": "Data",
			"fieldname": "degree",
			"width": 170
		},
	{
			"label": "capacity",
			"fieldtype": "Data",
			"fieldname": "capacity",
			"width": 170
		},
	{
			"label": "material",
			"fieldtype": "Data",
			"fieldname": "material",
			"width": 170
		},
	{
			"label": "oal",
			"fieldtype": "Data",
			"fieldname": "oal",
			"width": 170
		},
	{
			"label": "pin_box",
			"fieldtype": "Data",
			"fieldname": "pin_box",
			"width": 170
		},
	{
			"label": "id",
			"fieldtype": "Data",
			"fieldname": "id",
			"width": 170
		},
	{
			"label": "stroke",
			"fieldtype": "Data",
			"fieldname": "stroke",
			"width": 170
		},
	{
			"label": "pressure rating",
			"fieldtype": "Data",
			"fieldname": "pressure_rating",
			"width": 170
		},
	{
			"label": "gasket size rh",
			"fieldtype": "Data",
			"fieldname": "gasket_size_rh_",
			"width": 170
		},
		
		{
			"label": "no of stud bolts rh",
			"fieldtype": "Data",
			"fieldname": "no_of_stud_bolts_rh",
			"width": 170
		},
	
	{
			"label": "stud bolt size rh",
			"fieldtype": "Data",
			"fieldname": "stud_bolt_size_rh",
			"width": 170
		},
	{
			"label": "no of stud bolts lh",
			"fieldtype": "Data",
			"fieldname": "no_of_stud_bolts_lh_",
			"width": 170
		},
	{
			"label": "pressure rating rh",
			"fieldtype": "Data",
			"fieldname": "pressure_rating_rh",
			"width": 170
		},
	{
			"label": "ss ring groove",
			"fieldtype": "Data",
			"fieldname": "ss_ring_groove_",
			"width": 170
		},
	{
			"label": "gasket size lh",
			"fieldtype": "Data",
			"fieldname": "gasket_size_lh_",
			"width": 170
		},
	{
			"label": "part number",
			"fieldtype": "Data",
			"fieldname": "part_number",
			"width": 170
		},
	{
			"label": "plastic coating",
			"fieldtype": "Data",
			"fieldname": "plastic_coating",
			"width": 170
		},
	{
			"label": "hard banding",
			"fieldtype": "Data",
			"fieldname": "hard_banding_",
			"width": 170
		},
	{
			"label": "mandrel od",
			"fieldtype": "Data",
			"fieldname": "mandrel_od",
			"width": 170
		},
	{
			"label": "elvator recess",
			"fieldtype": "Data",
			"fieldname": "elvator_recess",
			"width": 170
		},
	{
			"label": "slip recess",
			"fieldtype": "Data",
			"fieldname": "slip_recess_",
			"width": 170
		},
	{
			"label": "psi",
			"fieldtype": "Data",
			"fieldname": "psi",
			"width": 170
		},
	{
			"label": "torque guage",
			"fieldtype": "Data",
			"fieldname": "torque_guage",
			"width": 170
		},
	{
			"label": "lift cylinders",
			"fieldtype": "Data",
			"fieldname": "lift_cylinders",
			"width": 170
		},

	{
			"label": "packing element",
			"fieldtype": "Data",
			"fieldname": "packing_element",
			"width": 170
		},
	
{
			"label": "style",
			"fieldtype": "Data",
			"fieldname": "style",
			"width": 170
		},
	{
			"label": "used for",
			"fieldtype": "Data",
			"fieldname": "used_for",
			"width": 170
		},
	{
			"label": "packer size",
			"fieldtype": "Data",
			"fieldname": "packer_size",
			"width": 170
		},
	
	]


	
	
	return columns
def get_data(filters):
	# all_asset = frappe.db.get_list('Asset',['*'])

	if filters.get('asset') : 
		all_asset = frappe.db.get_list('Asset',
    filters={
        'name': filters.get('asset') 
    },
    fields=['name' ,  'asset_name' ,'asset_category'  , 'location' , 'company' , 'status' , 'rental_status' , 'item_name' , 'item_code']
	)

	
	elif filters.get('asset_category') : 
		all_asset = frappe.db.get_list('Asset',
    filters={
        'asset_category': filters.get('asset_category') 
    },
    fields=['name' ,  'asset_name' ,'asset_category'  , 'location' , 'company' , 'status' , 'rental_status' , 'item_name' , 'item_code']
	)
	else : 
		all_asset = frappe.db.get_list('Asset', fields=['name' ,  'asset_name' ,'asset_category'  , 'location' , 'company' , 'status' , 'rental_status' , 'item_name' , 'item_code'])


	all_items = dict()
	final_list = list()
	for i in all_asset : 
		ass_dict = { 'asset_id' : i['name'] , 'asset_name' : i['asset_name'] , 'asset_category' : i['asset_category'] , 'location' : i['location'] , 
		'company' : i['company'] , 'status' : i['status'] , 'rental_status' : i['rental_status'] , 
		'item_name' : i['item_name'] , 'item_code' : i['item_code'] 
		
		}
		try:
			all_items[i['item_code']] 
		

		except: 
			if filters.get('parent_group'): 

				fetch_item = frappe.get_doc({'doctype' : 'Item' , 'item_group' : filters.get('parent_group')} )
			else : 
				fetch_item = frappe.get_doc('Item' , i['item_code'])
			all_items.update({i['item_code'] : { 'parent_group' : (frappe.get_doc('Item Group' , fetch_item.item_group)).parent_item_group, 'item_group' : fetch_item.item_group , 'type' : fetch_item.type , 'ppf' : fetch_item.ppf ,
			'tool_joint_id' :fetch_item.tool_joint_id , 'tool_joint_od' : fetch_item.tool_joint_od , 'range' : fetch_item.range , 
			'od_size_' : fetch_item.od_size_ , 'top_connection' : fetch_item.top_connection , 'bottom_connection' : fetch_item.bottom_connection , 
			'service' : fetch_item.service , 'make':fetch_item.make , 'size': fetch_item.size , 'pin_connection' : fetch_item.pin_connection , 
			'box_connection' : fetch_item.box_connection , 'od': fetch_item.od , 'wrap_angle' : fetch_item.wrap_angle , 'hard_facing' : fetch_item.hard_facing , 
			'model' : fetch_item.model , 'degree' : fetch_item.degree , 'capacity' : fetch_item.capacity , 'material' : fetch_item.material , 
			'oal' : fetch_item.oal , 'pin_box' : fetch_item.pin_box , 'id': fetch_item.id , 'stroke' : fetch_item.stroke , 
			'pressure_rating' : fetch_item.pressure_rating , 'gasket_size_rh_' : fetch_item.gasket_size_rh_ , 'no_of_stud_bolts_rh' : fetch_item.no_of_stud_bolts_rh , 
			'stud_bolt_size_rh'  : fetch_item.stud_bolt_size_rh , 'no_of_stud_bolts_lh_' : fetch_item.no_of_stud_bolts_lh_ , 'pressure_rating_rh' : fetch_item.pressure_rating_rh , 
			'ss_ring_groove_' : fetch_item.ss_ring_groove_ , 'gasket_size_lh_' : fetch_item.gasket_size_lh_ , 'part_number' : fetch_item.part_number , 'plastic_coating' : fetch_item.plastic_coating , 
			'hard_banding_' : fetch_item.hard_banding_ , 'mandrel_od' : fetch_item.mandrel_od , 'elvator_recess' : fetch_item.elvator_recess , 
			'slip_recess_' : fetch_item.slip_recess_ , 'psi' : fetch_item.psi , 'torque_guage' : fetch_item.torque_guage , 'lift_cylinders' : fetch_item.lift_cylinders , 
			'packing_element' : fetch_item.packing_element , 'style' : fetch_item.style , 'used_for' : fetch_item.used_for , 'packer_size' : fetch_item.packer_size
				
			}})
			ass_dict.update(all_items[i['item_code']] )


		ass_dict.update(all_items[i['item_code']] )
		
		final_list.append(ass_dict)


	return final_list

