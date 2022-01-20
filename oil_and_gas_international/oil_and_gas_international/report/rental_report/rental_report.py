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
            "label": "Asset Item Name",
            "fieldname": "asset_item_name",
            "fieldtype": "Link",
            "options": 'Item',
            "width": 100
        },
        {
            "label": "Grand Parent Group",
            "fieldname": "grand_parent_group",
            "fieldtype": "Link",
            "options":'Item Group',
        },
        {
            "label": "Parent Group",
            "fieldname": "parent_group",
            "fieldtype": "Link",
            "options":'Item Group',
        },
        {
            "label": "Child Group",
            "fieldname": "child_group",
            "fieldtype": "Link",
            "options":'Item Group',
        },
        {
            "label": "Total Assets",
            "fieldname": "asset_status",
            "fieldtype": "Data",
        },
        {
            "label": "Available",
            "fieldname": "available",
            "fieldtype": "Data",
        },
        {
            "label": "Rented",
            "fieldname": "rented",
            "fieldtype": "Data",
        },
        {
            "label": "Under Inspection",
            "fieldname": "under_inspection",
            "fieldtype": "Data",
        },
        
    ]
    itm_filter = {
        'is_fixed_asset': 1,
    }

    if filters.get("child_group"):
        itm_filter["item_group"] = filters.get("child_group")
    if filters.get("parent_group"):
        itm_filter["parent_group"] = filters.get("parent_group")
    if filters.get("grand_parent_group"):
        itm_filter["grand_parent_group"] = filters.get("grand_parent_group")
    item_list=frappe.db.get_list('Item',itm_filter,['*'])
    fields=fieldnames(item_list)
    for field_name in fields:
        columns.append({
            'label': fields[field_name],
            'fieldname': field_name,
            'fieldtype': 'Data',
            'width':100,
        })
    data = get_data(filters, columns,item_list)
    return columns, data




def get_data(filters, columns,items):
    data = []
    
    for row in items:
        status=frappe.db.count('Asset',{'item_code':row.item_code,'docstatus':1})
        available = frappe.db.count('Asset',{'item_code':row.item_code,'rental_status':'Available for Rent','docstatus':1})
        use = frappe.db.count('Asset',{'item_code':row.item_code,'rental_status':'In Use','docstatus':1})
        hold = frappe.db.count('Asset',{'item_code':row.item_code,'rental_status':'On hold for Inspection','docstatus':1})
        out_of_order = frappe.db.count('Asset',{'item_code':row.item_code,'status':'Out of Order','docstatus':1})
        fields=fieldnames_values(row)
        
        item_data ={
            'asset_item_name':row.item_code,
            'child_group':row.item_group,
            'parent_group':row.parent_group,
            'grand_parent_group':row.grand_parent_group,
            'asset_status':status,
            'available':available,
            'rented':use,
            'under_inspection':hold,
            # 'out_of_order':out_of_order,
        }
        for item in fields:
            item_data.update({
                item:fields[item]
            })
        data.append(item_data)
    return data

def fieldnames(item_list):
    field_list={}
    for row in item_list:
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
            
        if row.pressure_rating:
            if 'pressure_rating' not in field_list:
                field_list['pressure_rating']='Pressure Rating'
           
        if row.ppf:
            if 'ppf' not in field_list:
                field_list['ppf']='PPF'
            
        if row.tool_joint_od:
            if 'tool_joint_od' not in field_list:
                field_list['tool_joint_od']='Tool Joint OD'
            
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
          
        if row.id:
            if 'id' not in field_list:
                field_list['id']='ID'
           
        if row.mandrel_od:
            if 'mandrel_od' not in field_list:
                field_list['mandrel_od']='Mandrel OD'
           
        if row.stroke:
            if 'stroke' not in field_list:
                field_list['stroke']='Stroke'
           
        if row.wrap_angel:
            if 'wrap_angel' not in field_list:
                field_list['wrap_angel']='Wrap Angel'
            
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
        
    if row.pressure_rating:
        if 'pressure_rating' not in field_list:
            field_list['pressure_rating']=row.pressure_rating
        
    if row.ppf:
        if 'ppf' not in field_list:
            field_list['ppf']=row.ppf
        
    if row.tool_joint_od:
        if 'tool_joint_od' not in field_list:
            field_list['tool_joint_od']=row.tool_joint_od
        
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
        
    if row.id:
        if 'id' not in field_list:
            field_list['id']=row.id
        
    if row.mandrel_od:
        if 'mandrel_od' not in field_list:
            field_list['mandrel_od']=row.mandrel_od
        
    if row.stroke:
        if 'stroke' not in field_list:
            field_list['stroke']=row.stroke
        
    if row.wrap_angel:
        if 'wrap_angel' not in field_list:
            field_list['wrap_angel']=row.wrap_angel
        
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
    return field_list