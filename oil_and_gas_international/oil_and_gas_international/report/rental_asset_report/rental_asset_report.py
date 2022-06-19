# Copyright (c) 2022, Craft and contributors
# For license information, please see license.txt

from itertools import count
from typing import Counter

from numpy import take
import frappe
from frappe import _, get_all

# Done by Mr.index 0_0 A.M

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
			
		# {
		# 	"label": "Sub Category",
		# 	"fieldname": "parent_group",
		# 	"fieldtype": "Link",
		# 	"options":'Item Group',
		# 	"width": 130
		# },
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
	all_asset = frappe.db.get_list('Asset')
	# 057276699
	all_items = dict()
	# take_one = frappe.get_doc('Asset' , all_asset[0]['name'])
	# print(take_one)
	# print(take_one.item_code)
	# tt = frappe.get_doc('Item' , take_one.item_code)
	
	final_list = list()
	counter = 0 
	while counter < len(all_asset)   : 
		take_ass = frappe.get_doc('Asset' , all_asset[counter]['name'])
		get_item_name = take_ass.item_code
		ass_dict = { 'asset_id' : all_asset[counter]['name'] , 'asset_name' : take_ass.asset_name , 'asset_category' : take_ass.asset_category , 'location' : take_ass.location , 
		'company' : take_ass.company , 'status' : take_ass.status , 'rental_status' : take_ass.rental_status , 
		'item_name' : take_ass.item_name , 'item_code' : take_ass.item_code 
		
		}
		
		try:
			fetch_item = all_items[take_ass.item_code] 
		

		except: 
			fetch_item = frappe.get_doc('Item' , get_item_name)
			all_items.update({get_item_name : {'item_group' : fetch_item.item_group , 'type' : fetch_item.type , 'ppf' : fetch_item.ppf ,
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


		ass_dict.update(all_items[take_ass.item_code] )
		final_list.append(ass_dict)

		counter +=1 

	
	return final_list

