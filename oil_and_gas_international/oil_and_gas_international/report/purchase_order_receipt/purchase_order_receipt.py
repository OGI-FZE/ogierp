from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe.utils import getdate, flt

def execute(filters = None):
    columns = get_columns(filters)
    data = get_data(filters)
    print("columns",columns)
    print("execute data\n",data)
    return columns, data

def get_columns(filters):
    columns = [
        {
            'label':'Supplier',
            'field_type':'Link',
            'options':'Supplier',
            'field_name':'supplier',
            'width': 200
        },
        {
            'label':'Purchase Order',
            'field_type':'Link',
            'options':'Purchase Order',
            'field_name':'po',
            'width': 200
        },
        {
            'label':'Purchase Order',
            'field_type':'Data',
            'field_name':'poo',
            'width': 200
        }
    ]
    return columns

def get_data(filters):
    data = []
    sql = '''select name,supplier from `tabPurchase Order`'''
    purchase_ord_no = frappe.db.sql(sql,as_dict = True)
    
    for p in purchase_ord_no:
        # print("================")
        # print(p.name)
        # print("================")
        print(type(p.name))
        po = frappe.get_doc("Purchase Order",p.name)
        row = {
            'po':po.name,
            'poo':po.name,
            'supplier':p.supplier
            }
    # row = {
    #     'name':'abc'
    # }
        print("================")
        print(row)
        data.append(row)
    return data