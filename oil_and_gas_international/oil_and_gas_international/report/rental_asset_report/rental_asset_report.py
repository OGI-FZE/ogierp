# Copyright (c) 2013, Havenir Solutions Private Limited and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe.utils import add_to_date
from frappe import _
from dateutil.relativedelta import relativedelta


def execute(filters=None):
	columns= [
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
			"fieldname": "grand_parent_group",
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
			"fieldname": "child_group",
			"fieldtype": "Link",
			"options":'Item Group',
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
		
	]

	asset_filter = {
		'docstatus': 1,
	}


	if filters.get("asset"):
		asset_filter["name"] = filters.get("asset")
	if filters.get("child_group"):
		asset_filter["item_group"] = filters.get("child_group")

		
	asset_list=frappe.db.get_list('Asset',asset_filter,['*'])

	if filters.get("parent_group"):
		asset_filter["parent_group"] = filters.get("parent_group")
	if filters.get("grand_parent_group"):
		asset_filter["grand_parent_group"] = filters.get("grand_parent_group")


	filtered_list=[]

	# for row in asset_list:
	# 	itm = frappe.get_doc("Item",row.item_code)
	# 	item_group = itm.item_group
	# 	parent_group = frappe.db.get_value('Item Group',itm.item_group,['parent_item_group'])
	# 	if frappe.db.exists({
	# 			'doctype': 'Item Group',
	# 			'name': parent_group,
	# 		}):
	# 		g_parent=frappe.db.get_value('Item Group',parent_group,['parent_item_group'])
	# 		if g_parent==asset_filter["grand_parent_group"] and asset_filter["parent_group"]==parent_group:
	# 			filtered_list.append(row)

	if not filters.get("grand_parent_group") and not filters.get("parent_group"):
		filtered_list=asset_list

	if filters.get("grand_parent_group") and filters.get("parent_group"):
		for row in asset_list:
			itm = frappe.get_doc("Item",row.item_code)
			parent_group = frappe.db.get_value('Item Group',itm.item_group,['parent_item_group'])
			if frappe.db.exists({
					'doctype': 'Item Group',
					'name': parent_group,
				}):
				g_parent=frappe.db.get_value('Item Group',parent_group,['parent_item_group'])
				if g_parent==asset_filter["grand_parent_group"] and asset_filter["parent_group"]==parent_group:
					filtered_list.append(row)

	if filters.get("grand_parent_group") and not filters.get("parent_group"):
		for row in asset_list:
			itm = frappe.get_doc("Item",row.item_code)
			parent_group = frappe.db.get_value('Item Group',itm.item_group,['parent_item_group'])
			if frappe.db.exists({
					'doctype': 'Item Group',
					'name': parent_group,
				}):
				g_parent=frappe.db.get_value('Item Group',parent_group,['parent_item_group'])
				if g_parent==asset_filter["grand_parent_group"]:
					filtered_list.append(row)
	
	if filters.get("parent_group") and not filters.get("grand_parent_group"):
		for row in asset_list:
			itm = frappe.get_doc("Item",row.item_code)
			parent_group = frappe.db.get_value('Item Group',itm.item_group,['parent_item_group'])
			if frappe.db.exists({
					'doctype': 'Item Group',
					'name': parent_group,
				}):
				g_parent=frappe.db.get_value('Item Group',parent_group,['parent_item_group'])
				if parent_group==asset_filter["parent_group"]:
					filtered_list.append(row)
	

	fields=fieldnames(filtered_list)
	for field_name in fields:
		columns.append({
			'label': fields[field_name],
			'fieldname': field_name,
			'fieldtype': 'Data',
			'width':100,
		})
	data = get_data(filtered_list)
	return columns, data


def get_data(asset_list):
	data = []
	
	for row in asset_list: 
		pg = '' 
		gpg = '' 
		item = frappe.get_doc('Item',row.item_code) 
		fields=fieldnames_values(item) 
		parent_group = frappe.db.get_value('Item Group',item.item_group,['parent_item_group'])
		if parent_group:
			pg = parent_group
			gpg=frappe.db.get_value('Item Group',parent_group,['parent_item_group'])
		
		asset_data ={
			'asset_id':row.name,
			'asset_name':row.asset_name,
			'child_group':item.item_group,
			'parent_group':pg,
			'grand_parent_group':gpg,
			'status':row.status,
			'rental_status':row.rental_status,
		}

		for asset in fields:
			asset_data.update({
				asset:fields[asset]
			})

		data.append(asset_data)

	return data

def fieldnames(item_list):
	field_list={}
	for row in item_list:
		row = frappe.get_doc("Item",row.item_code)
		if row.make:
			if 'make' not in field_list:
				field_list['make']='Make'
		if row.model:
			if 'model' not in field_list:
				field_list['model']='Model'
		if row.size:
			if 'size' not in field_list:
				field_list['size']='Size'
		   
		if row.part_number:
			if 'part_number' not in field_list:
				field_list['part_number']='Part Number'
			
		if row.type:
			if 'type' not in field_list:
				field_list['type']='Type'
		   
		if row.material:
			if 'material' not in field_list:
				field_list['material']='Material'

		if row.plastic_coating:
			if 'plastic_coating' not in field_list:
				field_list['plastic_coating']='PLASTIC COATING'

			
		if row.pressure_rating:
			if 'pressure_rating' not in field_list:
				field_list['pressure_rating']='Pressure Rating'
		   
		if row.ppf:
			if 'ppf' not in field_list:
				field_list['ppf']='PPF'
			
		if row.tool_joint_id:
			if 'tool_joint_id' not in field_list:
				field_list['tool_joint_id']='Tool Joint ID'

		if row.tool_joint_od:
			if 'tool_joint_od' not in field_list:
				field_list['tool_joint_od']='Tool Joint OD'

		if row.hard_banding_:
			if 'hard_banding_' not in field_list:
				field_list['hard_banding_']='Hard Banding'

		if row.gasket_size_rh_:
			if 'gasket_size_rh_' not in field_list:
				field_list['gasket_size_rh_']='GASKET SIZE RH'
			
		if row.no_of_stud_bolts_rh:
			if 'no_of_stud_bolts_rh' not in field_list:
				field_list['no_of_stud_bolts_rh']='No of Stud Bolts RH'
			
		if row.stud_bolt_size_rh:
			if 'stud_bolt_size_rh' not in field_list:
				field_list['stud_bolt_size_rh']='Stud Bolt Size RH'
			
		if row.no_of_stud_bolts_lh_:
			if 'no_of_stud_bolts_lh_' not in field_list:
				field_list['no_of_stud_bolts_lh_']='No of Stud Bolts LH'
			
		if row.pin_box:
			if 'pin_box' not in field_list:
				field_list['pin_box']='Pin/Box'
			
		if row.pin_connection:
			if 'pin_connection' not in field_list:
				field_list['pin_connection']='Pin Connection'
		   
		if row.box_connection:
			if 'box_connection' not in field_list:
				field_list['box_connection']='Box Connection'
			
		if row.range:
			if 'range' not in field_list:
				field_list['range']='Range'
			
		if row.oal:
			if 'oal' not in field_list:
				field_list['oal']='Oal'
		   
		if row.od:
			if 'od' not in field_list:
				field_list['od']='OD'

		if row.od_size_:
			if 'od_size_' not in field_list:
				field_list['od_size_']='OD size'
		  
		if row.id:
			if 'id' not in field_list:
				field_list['id']='ID'
		   
		if row.mandrel_od:
			if 'mandrel_od' not in field_list:
				field_list['mandrel_od']='Mandrel OD'
		   
		if row.top_connection:
			if 'top_connection' not in field_list:
				field_list['top_connection']='Top Connection'
		   
		if row.bottom_connection:
			if 'bottom_connection' not in field_list:
				field_list['bottom_connection']='Bottom Connection'
		   
		if row.elvator_recess:
			if 'elvator_recess' not in field_list:
				field_list['elvator_recess']='ELVATOR RECESS'
		   
		if row.slip_recess_:
			if 'slip_recess_' not in field_list:
				field_list['slip_recess_']='SLIP RECESS'
		   
		if row.service:
			if 'service' not in field_list:
				field_list['service']='SERVICE'
		   
		if row.stud_bolt_size_lh_:
			if 'stud_bolt_size_lh_' not in field_list:
				field_list['stud_bolt_size_lh_']='Stud Bolt Size LH'
		   
		if row.packer_size:
			if 'packer_size' not in field_list:
				field_list['packer_size']='PACKER SIZE'
		   
		if row.stroke:
			if 'stroke' not in field_list:
				field_list['stroke']='Stroke'
		   
		if row.wrap_angle:
			if 'wrap_angle' not in field_list:
				field_list['wrap_angle']='Wrap Angel'
			
		if row.hard_facing:
			if 'hard_facing' not in field_list:
				field_list['hard_facing']='Hard Facing'
			
		if row.capacity:
			if 'capacity' not in field_list:
				field_list['capacity']='Capacity'
			
		if row.degree:
			if 'degree' not in field_list:
				field_list['degree']='Degree'
			
		if row.psi:
			if 'psi' not in field_list:
				field_list['psi']='PSI'
			
		if row.torque_guage:
			if 'torque_guage' not in field_list:
				field_list['torque_guage']='Torque Guage'
			
		if row.lift_cylinders:
			if 'lift_cylinders' not in field_list:
				field_list['lift_cylinders']='Lift Cylinders'

		if row.pressure_rating_rh:
			if 'pressure_rating_rh' not in field_list:
				field_list['pressure_rating_rh']='PRESSURE RATING RH'

		if row.ss_ring_groove_:
			if 'ss_ring_groove_' not in field_list:
				field_list['ss_ring_groove_']='SS RING GROOVE'

		if row.packing_element:
			if 'packing_element' not in field_list:
				field_list['packing_element']='PACKING ELEMENT'

		if row.style:
			if 'style' not in field_list:
				field_list['style']='STYLE'

		if row.used_for:
			if 'used_for' not in field_list:
				field_list['used_for']='USED FOR'

		if row.gasket_size_lh_:
			if 'gasket_size_lh_' not in field_list:
				field_list['gasket_size_lh_']='GASKET SIZE LH'

	return field_list

def fieldnames_values(row):
	field_list={}
	if row.make:
		if 'make' not in field_list:
			field_list['make']=row.make
	if row.model:
		if 'model' not in field_list:
			field_list['model']=row.model
	if row.size:
		if 'size' not in field_list:
			field_list['size']=row.size
		
	if row.part_number:
		if 'part_number' not in field_list:
			field_list['part_number']=row.part_number
		
	if row.type:
		if 'type' not in field_list:
			field_list['type']=row.type
		
	if row.material:
		if 'material' not in field_list:
			field_list['material']=row.material

	if row.plastic_coating:
		if 'plastic_coating' not in field_list:
			field_list['plastic_coating']=row.plastic_coating
		
	if row.pressure_rating:
		if 'pressure_rating' not in field_list:
			field_list['pressure_rating']=row.pressure_rating
		
	if row.ppf:
		if 'ppf' not in field_list:
			field_list['ppf']=row.ppf

	if row.tool_joint_id:
		if 'tool_joint_id' not in field_list:
			field_list['tool_joint_id']=row.tool_joint_id
		
	if row.tool_joint_od:
		if 'tool_joint_od' not in field_list:
			field_list['tool_joint_od']=row.tool_joint_od

	if row.hard_banding_:
		if 'hard_banding_' not in field_list:
			field_list['hard_banding_']=row.hard_banding_

	if row.gasket_size_rh_:
		if 'gasket_size_rh_' not in field_list:
			field_list['gasket_size_rh_']=row.gasket_size_rh_

	if row.no_of_stud_bolts_rh:
		if 'no_of_stud_bolts_rh' not in field_list:
			field_list['no_of_stud_bolts_rh']=row.no_of_stud_bolts_rh

	if row.stud_bolt_size_rh:
		if 'stud_bolt_size_rh' not in field_list:
			field_list['stud_bolt_size_rh']=row.stud_bolt_size_rh

	if row.no_of_stud_bolts_lh_:
		if 'no_of_stud_bolts_lh_' not in field_list:
			field_list['no_of_stud_bolts_lh_']=row.no_of_stud_bolts_lh_

	if row.packer_size:
		if 'packer_size' not in field_list:
			field_list['packer_size']=row.packer_size
		
	if row.pin_box:
		if 'pin_box' not in field_list:
			field_list['pin_box']=row.pin_box
		
	if row.pin_connection:
		if 'pin_connection' not in field_list:
			field_list['pin_connection']=row.pin_connection
		
	if row.box_connection:
		if 'box_connection' not in field_list:
			field_list['box_connection']=row.box_connection
		
	if row.range:
		if 'range' not in field_list:
			field_list['range']=row.range
		
	if row.oal:
		if 'oal' not in field_list:
			field_list['oal']=row.oal
		
	if row.od:
		if 'od' not in field_list:
			field_list['od']=row.od
		
	if row.od_size_:
		if 'od_size_' not in field_list:
			field_list['od_size_']=row.od_size_
		
	if row.id:
		if 'id' not in field_list:
			field_list['id']=row.id
		
	if row.mandrel_od:
		if 'mandrel_od' not in field_list:
			field_list['mandrel_od']=row.mandrel_od

	if row.top_connection:
		if 'top_connection' not in field_list:
			field_list['top_connection']=row.top_connection

	if row.bottom_connection:
		if 'bottom_connection' not in field_list:
			field_list['bottom_connection']=row.bottom_connection

	if row.elvator_recess:
		if 'elvator_recess' not in field_list:
			field_list['elvator_recess']=row.elvator_recess

	if row.slip_recess_:
		if 'slip_recess_' not in field_list:
			field_list['slip_recess_']=row.slip_recess_

	if row.service:
		if 'service' not in field_list:
			field_list['service']=row.service

	if row.stud_bolt_size_lh_:
		if 'stud_bolt_size_lh_' not in field_list:
			field_list['stud_bolt_size_lh_']=row.stud_bolt_size_lh_
		
	if row.stroke:
		if 'stroke' not in field_list:
			field_list['stroke']=row.stroke
		
	if row.wrap_angle:
		if 'wrap_angle' not in field_list:
			field_list['wrap_angle']=row.wrap_angle
		
	if row.hard_facing:
		if 'hard_facing' not in field_list:
			field_list['hard_facing']=row.hard_facing
		
	if row.capacity:
		if 'capacity' not in field_list:
			field_list['capacity']=row.capacity
		
	if row.degree:
		if 'degree' not in field_list:
			field_list['degree']=row.degree
		
	if row.psi:
		if 'psi' not in field_list:
			field_list['psi']=row.psi
		
	if row.torque_guage:
		if 'torque_guage' not in field_list:
			field_list['torque_guage']=row.torque_guage
		
	if row.lift_cylinders:
		if 'lift_cylinders' not in field_list:
			field_list['lift_cylinders']=row.lift_cylinders

	if row.pressure_rating_rh:
		if 'pressure_rating_rh' not in field_list:
			field_list['pressure_rating_rh']=row.pressure_rating_rh

	if row.ss_ring_groove_:
		if 'ss_ring_groove_' not in field_list:
			field_list['ss_ring_groove_']=row.ss_ring_groove_

	if row.packing_element:
		if 'packing_element' not in field_list:
			field_list['packing_element']=row.packing_element

	if row.style:
		if 'style' not in field_list:
			field_list['style']=row.style

	if row.used_for:
		if 'used_for' not in field_list:
			field_list['used_for']=row.used_for

	if row.gasket_size_lh_:
		if 'gasket_size_lh_' not in field_list:
			field_list['gasket_size_lh_']=row.gasket_size_lh_

	return field_list