# Copyright (c) 2022, Craft and contributors
# For license information, please see license.txt

from colorsys import ONE_THIRD
from itertools import count
from typing import Counter

from numpy import take
import frappe
from frappe import _, get_all

# DONE by MR.index 0_0 A.M - enhanced algorithm-24 seconds to render
def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		# {
		# 	"label": "Asset Item Name",
		# 	"fieldname": "asset_item",
		# 	"fieldtype": "Link",
		# 	"options": 'Asset',
		# 	"width": 130
		# },
		# {
		# 	"label": "Asset Name",
		# 	"fieldname": "asset_name",
		# 	"fieldtype": "Data",
		# 	"width": 150
		# },
		
		# {
		# 	"label": "location",
		# 	"fieldname": "location",
		# 	"fieldtype": "Link",
		# 	"options":'Location',
		# 	"width": 130
		# },


		# {
		# 	"label": "Company",
		# 	"fieldname": "company",
		# 	"fieldtype": "Link",
		# 	"options":'Company',
		# 	"width": 130
		# },
# {
# 			"label": "Status",
# 			"fieldtype": "Data",
# 			"fieldname": "status",
# 			"width": 150
# 		},
		# {
		# 	"label": "Rental Status",
		# 	"fieldtype": "Select",
		# 	"fieldname": "rental_status",
		# 	"width": 170
		# },

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
			"label": "Category",
			"fieldname": "asset_category",
			"fieldtype": "Link",
			"options":'Item Group',
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
			"label": "Total assets",
			"fieldname": "total_assets",
			"fieldtype": "Data",
			"width": 130
		},
        {
			"label": "Available",
			"fieldname": "available",
			"fieldtype": "Data",
			"width": 130
		},
        {
			"label": "Rented",
			"fieldname": "rented",
			"fieldtype": "Data",
			"width": 130
		},
        {
			"label": "Under inspection",
			"fieldname": "under_inspection",
			"fieldtype": "Data",
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
	if filters.get('item_code') : 
		all_asset = frappe.db.get_list('Item',
    filters={
        'name': filters.get('item_code') 
    },
    fields=['name' ,'item_name' , 'item_code' , 'asset_category' , 'item_group' , 'type' , 'ppf' , 'tool_joint_id' , 'tool_joint_od' , 'range' , 
    'od_size_' , 'top_connection' , 'bottom_connection' , 'service' , 'make' , 'size' , 'pin_connection' , 'box_connection' , 'od' , 
    'wrap_angle' , 'hard_facing' , 'model' , 'degree' , 'capacity' , 'material' , 'oal' , 'pin_box' , 'id' , 'stroke' , 'pressure_rating' ,
    'gasket_size_rh_' , 'no_of_stud_bolts_rh' , 'stud_bolt_size_rh' , 'no_of_stud_bolts_lh_' , 'pressure_rating_rh' , 'ss_ring_groove_' , 
	'gasket_size_lh_' , 'part_number' , 'plastic_coating' , 'hard_banding_' , 'mandrel_od' , 'elvator_recess' , 'slip_recess_' , 'psi' , 
	'torque_guage' , 'lift_cylinders' , 'packing_element' , 'style' , 'used_for' ,'packer_size' , ''
    ]
	)

	
	elif filters.get('grand_parent_group') : 
		all_asset = frappe.db.get_list('Item',
    filters={
        'asset_category': filters.get('grand_parent_group') 
    },
   fields=['name' ,'item_name' ,'item_code' , 'asset_category' , 'item_group' , 'type' , 'ppf' , 'tool_joint_id' , 'tool_joint_od' , 'range' , 
    'od_size_' , 'top_connection' , 'bottom_connection' , 'service' , 'make' , 'size' , 'pin_connection' , 'box_connection' , 'od' , 
    'wrap_angle' , 'hard_facing' , 'model' , 'degree' , 'capacity' , 'material' , 'oal' , 'pin_box' , 'id' , 'stroke' , 'pressure_rating' ,
    'gasket_size_rh_' , 'no_of_stud_bolts_rh' , 'stud_bolt_size_rh' , 'no_of_stud_bolts_lh_' , 'pressure_rating_rh' , 'ss_ring_groove_' , 
	'gasket_size_lh_' , 'part_number' , 'plastic_coating' , 'hard_banding_' , 'mandrel_od' , 'elvator_recess' , 'slip_recess_' , 'psi' , 
	'torque_guage' , 'lift_cylinders' , 'packing_element' , 'style' , 'used_for' ,'packer_size' , ''
    ]
	)
	elif filters.get('parent_group') : 
		all_asset = frappe.db.get_list('Item',
    filters={
        'item_group': filters.get('parent_group') 
    },
   fields=['name' ,'item_name' ,'item_code' , 'asset_category' , 'item_group' , 'type' , 'ppf' , 'tool_joint_id' , 'tool_joint_od' , 'range' , 
    'od_size_' , 'top_connection' , 'bottom_connection' , 'service' , 'make' , 'size' , 'pin_connection' , 'box_connection' , 'od' , 
    'wrap_angle' , 'hard_facing' , 'model' , 'degree' , 'capacity' , 'material' , 'oal' , 'pin_box' , 'id' , 'stroke' , 'pressure_rating' ,
    'gasket_size_rh_' , 'no_of_stud_bolts_rh' , 'stud_bolt_size_rh' , 'no_of_stud_bolts_lh_' , 'pressure_rating_rh' , 'ss_ring_groove_' , 
	'gasket_size_lh_' , 'part_number' , 'plastic_coating' , 'hard_banding_' , 'mandrel_od' , 'elvator_recess' , 'slip_recess_' , 'psi' , 
	'torque_guage' , 'lift_cylinders' , 'packing_element' , 'style' , 'used_for' ,'packer_size' , ''
    ]
	)
	else : 
		all_asset = frappe.db.get_list('Item', 
		fields=['name' ,'item_name' ,'item_code' , 'asset_category' , 'item_group' , 'type' , 'ppf' , 'tool_joint_id' , 'tool_joint_od' , 'range' , 
    'od_size_' , 'top_connection' , 'bottom_connection' , 'service' , 'make' , 'size' , 'pin_connection' , 'box_connection' , 'od' , 
    'wrap_angle' , 'hard_facing' , 'model' , 'degree' , 'capacity' , 'material' , 'oal' , 'pin_box' , 'id' , 'stroke' , 'pressure_rating' ,
    'gasket_size_rh_' , 'no_of_stud_bolts_rh' , 'stud_bolt_size_rh' , 'no_of_stud_bolts_lh_' , 'pressure_rating_rh' , 'ss_ring_groove_' , 
	'gasket_size_lh_' , 'part_number' , 'plastic_coating' , 'hard_banding_' , 'mandrel_od' , 'elvator_recess' , 'slip_recess_' , 'psi' , 
	'torque_guage' , 'lift_cylinders' , 'packing_element' , 'style' , 'used_for' ,'packer_size' , ''
    ]
		)


	# all_items = dict()
	final_list = list()
	full_assets = frappe.db.get_list('Asset', fields=[ 'rental_status'  , 'item_code' , 'docstatus'])



	for i in all_asset : 
		counter = 0 
		no_asset = no_ava = no_use = no_hold = 0;
		while counter < len(full_assets) :  
			if full_assets[counter]['item_code'] == i['item_code'] and full_assets[counter]['docstatus'] == 1 :
				no_asset +=1 
				if  full_assets[counter]['rental_status'] == 'Available for Rent' : 
					no_ava +=1 
					full_assets.remove(full_assets[counter])
				elif full_assets[counter]['rental_status'] == 'In Use' :
					no_use +=1 
					full_assets.remove(full_assets[counter])

				elif  full_assets[counter]['rental_status'] == 'On hold for Inspection' :
					no_hold +=1
					full_assets.remove(full_assets[counter])

			else : 
				counter +=1 

		i.update({'total_assets' : no_asset , 'available' : no_ava , 'rented' : no_use , 'under_inspection' : no_hold , 'parent_group' : (frappe.get_doc('Item Group' ,i['item_group'])).parent_item_group   })

		final_list.append(i)

		
		
		
		
		


	return final_list

