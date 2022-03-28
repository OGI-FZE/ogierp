from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe.utils import getdate, flt

def execute(filters = None):
    if not filters:filters={}
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions,filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
			"label": _("Purchase Order"),
			"fieldname": "p_o",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 200
		},
        {
            'label':_('Purchase Receipt'),
            'fieldname':'p_r',
            'fieldtype':'Link',
            'options':'Purchase Receipt',
            'width': 200
        },
        {
            'label':_('Supplier'),
            'fieldname':'supplier',
            'fieldtype':'Link',
            'options':'Supplier',
            'width': 200
        },
        {
            'label':_('Item'),
            'fieldname':'i_n',
            'fieldtype':'Link',
            'options':'Item',
            'width': 200
        },
        {
            'label':'Quantity',
            'fieldtype':'float',
            'fieldname':'qty',
            'width': 100
        },
        {
            'label':'Amount',
            'fieldtype':'currency',
            'fieldname':'amt',
            'width': 100
        },
        {
            'label':'Required By',
            'fieldtype':'Date',
            'fieldname':'req_by',
            'width': 100
        },
        {
            'label':'Purchase Receipt Date',
            'fieldtype':'Date',
            'fieldname':'pr_date',
            'width': 100
        },
        {
            'label':'Date Difference',
            'fieldtype':'float',
            'fieldname':'date_diff',
            'width': 100
        },
    ]
    return columns

def get_data(conditions,filters):
    data = frappe.db.sql(
        '''select 
        pri.purchase_order as p_o, pri.parent as p_r, po.supplier as supplier, 
        pri.item_name as i_n, pri.qty as qty, pri.amount as amt,
        po.schedule_date as req_by, pr.posting_date as pr_date, 
        datediff(pr.posting_date,po.schedule_date)
        from `tabPurchase Receipt Item` pri 
        left join `tabPurchase Order` po 
        on pri.purchase_order = po.name
        left join `tabPurchase Receipt` pr on pr.name = pri.parent {} order by po.creation desc'''.format(conditions, filters)
    )
    return data

def get_conditions(filters):
    conditions = ''
    if filters.get('from_date') and filters.get('to_date'):
        conditions += 'where po.transaction_date between "{}" and "{}"'.format(filters.get('from_date'),filters.get('to_date'))

    if filters.get('supplier'):
        conditions += 'where po.supplier = "{}"'.format(filters.get('supplier'))

    return conditions