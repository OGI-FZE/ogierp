# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
from multiprocessing import Condition
import frappe
from frappe import _

def execute(filters=None):
	if not filters:filters={}
	conditions = get_conditions(filters)
	columns, data = get_columns(filters), get_data(conditions,filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			'label': _('Asset Code'),
			'field_name':'asset_code',
			'fieldtype':'Link',
			'options':'Asset',
			'width':200
		},
		{
			'label': _('Asset Name'),
			'field_name':'asset_name',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label': _('Asset Location'),
			'field_name':'asset_location',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label': _('Customer Name'),
			'field_name':'customer_name',
			'fieldtype':'Data',
			'width':200
		},
		{
			'label': _('Hired On'),
			'field_name':'date',
			'fieldtype':'Date',
			'width':200
		},
	]

	return columns

def get_data(conditions,filters):
	data = frappe.db.sql(
		'''select
		a.name, a.asset_name, a.location, rin.customer_name, rin.date from
		`tabRental Issue Note Item` rini join `tabAsset` a on
		a.name like substring_index(rini.assets,'\n',1)  join `tabRental Issue Note` rin on
		rin.name = rini.parent
		where a.rental_status = "In Use" {} order by rin.creation desc'''.format(conditions, filters)
	)
	return data

def get_conditions(filters):
	conditions = ''

	if filters.get('asset_code'):
		conditions += 'and a.name = "{}"'.format(filters.get('asset_code'))

	return conditions

