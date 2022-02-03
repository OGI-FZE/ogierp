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
            "label": "Category",
            "fieldname": "grand_parent_group",
            "fieldtype": "Link",
            "options":'Item Group',
        },
        {
            "label": "Sub Category",
            "fieldname": "parent_group",
            "fieldtype": "Link",
            "options":'Item Group',
        },
        {
            "label": "Child Category",
            "fieldname": "child_group",
            "fieldtype": "Link",
            "options":'Item Group',
        },
        
    ]
    itm_filter = {
        'is_fixed_asset': 1,
    }

    if filters.get("item_code"):
        itm_filter["item_code"] = filters.get("item_code")
    if filters.get("child_group"):
        itm_filter["item_group"] = filters.get("child_group")
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
        fields=fieldnames_values(row) 
        parent_group = frappe.db.get_value('Item Group',row.item_group,['parent_item_group'])
        g_parent=''
        if frappe.db.exists({
                'doctype': 'Item Group',
                'name': parent_group,
            }):
            g_parent=frappe.db.get_value('Item Group',parent_group,['parent_item_group'])
        item_data ={
            'asset_item_name':row.item_code,
            'child_group':row.item_group,
            'parent_group':parent_group,
            'grand_parent_group':g_parent,
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

        if row.tool_joint_id:
            if 'tool_joint_id' not in field_list:
                field_list['tool_joint_id']='Tool Joint ID'

            
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

        if row.hard_banding_:
            if 'hard_banding_' not in field_list:
                field_list['hard_banding_']='Hard Banding'

        if row.gasket_size_rh_:
            if 'gasket_size_rh_' not in field_list:
                field_list['gasket_size_rh_']='GASKET SIZE RH '

        if row.stud_bolt_size_rh:
            if 'stud_bolt_size_rh' not in field_list:
                field_list['stud_bolt_size_rh']='Stud Bolt Size RH'

        if row.no_of_stud_bolts_rh:
            if 'no_of_stud_bolts_rh' not in field_list:
                field_list['no_of_stud_bolts_rh']='No of Stud Bolts RH'

        if row.stud_bolt_size_lh_:
            if 'stud_bolt_size_lh_' not in field_list:
                field_list['stud_bolt_size_lh_']='Stud Bolt Size LH '

        if row.no_of_stud_bolts_lh_:
            if 'no_of_stud_bolts_lh_' not in field_list:
                field_list['no_of_stud_bolts_lh_']='No of Stud Bolts LH'

        if row.ss_ring_groove_:
            if 'ss_ring_groove_' not in field_list:
                field_list['ss_ring_groove_']='PACKING ELEMENT'

        if row.style:
            if 'style' not in field_list:
                field_list['style']='STYLE'

        if row.used_for:
            if 'used_for' not in field_list:
                field_list['used_for']='USED FOR'

        if row.packer_size:
            if 'packer_size' not in field_list:
                field_list['packer_size']='PACKER SIZE'

        if row.gasket_size_lh_:
            if 'gasket_size_lh_' not in field_list:
                field_list['gasket_size_lh_']='GASKET SIZE LH'

        if row.slip_recess_:
            if 'slip_recess_' not in field_list:
                field_list['slip_recess_']='SLIP RECESS '

        if row.pressure_rating_rh:
            if 'pressure_rating_rh' not in field_list:
                field_list['pressure_rating_rh']='PRESSURE RATING RH'

        if row.service:
            if 'service' not in field_list:
                field_list['service']='SERVICE'



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

    if row.tool_joint_id:
        if 'tool_joint_id' not in field_list:
            field_list['tool_joint_id']=row.tool_joint_id
        
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

    if row.hard_banding_:
        if 'hard_banding_' not in field_list:
            field_list['hard_banding_']=row.hard_banding_

    if row.gasket_size_rh_:
        if 'gasket_size_rh_' not in field_list:
            field_list['gasket_size_rh_']=row.gasket_size_rh_

    if row.stud_bolt_size_rh:
        if 'stud_bolt_size_rh' not in field_list:
            field_list['stud_bolt_size_rh']=row.stud_bolt_size_rh

    if row.no_of_stud_bolts_rh:
        if 'no_of_stud_bolts_rh' not in field_list:
            field_list['no_of_stud_bolts_rh']=row.no_of_stud_bolts_rh

    if row.stud_bolt_size_lh_:
        if 'stud_bolt_size_lh_' not in field_list:
            field_list['stud_bolt_size_lh_']=row.stud_bolt_size_lh_

    if row.no_of_stud_bolts_lh_:
        if 'no_of_stud_bolts_lh_' not in field_list:
            field_list['no_of_stud_bolts_lh_']=row.no_of_stud_bolts_lh_

    if row.ss_ring_groove_:
        if 'ss_ring_groove_' not in field_list:
            field_list['ss_ring_groove_']=row.ss_ring_groove_

    if row.style:
        if 'style' not in field_list:
            field_list['style']=row.style

    if row.used_for:
        if 'used_for' not in field_list:
            field_list['used_for']=row.used_for

    if row.packer_size:
        if 'packer_size' not in field_list:
            field_list['packer_size']=row.packer_size

    if row.gasket_size_lh_:
        if 'gasket_size_lh_' not in field_list:
            field_list['gasket_size_lh_']=row.gasket_size_lh_

    if row.slip_recess_:
        if 'slip_recess_' not in field_list:
            field_list['slip_recess_']=row.slip_recess_

    if row.pressure_rating_rh:
        if 'pressure_rating_rh' not in field_list:
            field_list['pressure_rating_rh']=row.pressure_rating_rh

    if row.service:
        if 'service' not in field_list:
            field_list['service']=row.service

    return field_list