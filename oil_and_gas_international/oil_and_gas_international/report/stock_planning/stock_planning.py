# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_data(filters):
	query = f"""
		SELECT
			item_type as description,
			item_group as item_group,
			quantity as plan_qty,
			uom as unit,
			rate as rate,
			total as total,
			company as company,
			posting_date as date,
			fiscal_year as fiscal_year
		FROM
			`tabStock Forecasting` as sf
		WHERE
			forcast_type = "Item"
		"""

	if filters.company:
		query = f"{query} AND company={frappe.db.escape(filters.company)}"

	if filters.from_date and filters.to_date:
		query = f"{query} AND posting_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'"

	if filters.fiscal_year:
		query = f"{query} AND fiscal_year = '{filters.fiscal_year}'"

	sql_data = frappe.db.sql(query, as_dict=True)
	
	item_group_query = f"""
		SELECT
			item_type as description,
			item_group as item_group,
			quantity as plan_qty,
			uom as unit,
			rate as rate,
			total as total,
			company as company,
			posting_date as date,
			fiscal_year as fiscal_year
		FROM
			`tabStock Forecasting` as sf
		WHERE
			forcast_type = "Item Group" AND company = "%s"
		""" %(filters.company)


	if filters.from_date and filters.to_date:
		item_group_query = f"{item_group_query} AND posting_date BETWEEN '{filters.from_date}' AND '{filters.to_date}'"

	if filters.fiscal_year:
		item_group_query = f"{item_group_query} AND fiscal_year = '{filters.fiscal_year}'"

	item_group_data = frappe.db.sql(item_group_query, as_dict=True)

	data = {}
	print("\n \n \n")
	for i in sql_data:
		item_code = i['description']
		company = i['company']
		stock_quantity = get_quantity(item_code, company) 
		i.update({"stock_qty": stock_quantity[0].get("actual_qty"), "company": company})
		data.setdefault(i['item_group'], []).append(i)

	result = []
	if data:	
		print(data)					
		for d in data:
			if d:
				group_row = {}
				group_row['trunk'] = d or ''
				group_row['indent'] = 0
				group_row['item_group'] = ""
				group_row['stock_qty'] = 0
				result.append(group_row)
				for i in data[d]:
					i['trunk'] = i['description']
					i['indent'] = 1
					result.append(i)
	groups = frappe.utils.unique([group.get("item_group") for group in result])

	for group in item_group_data:
		print(item_group_data)
		if not group['description'] in groups:
			result.append({
				'trunk': group['description'],
				'indent': 0,
				'stock_qty':get_group_qty(group['description'],filters.company),
				'plan_qty': group['plan_qty'],
				'rate': group['rate'],
				'total': group['total'],
			})
		
	for res in result:
		if res['indent'] == 0:
			for group in item_group_data:
				if res['trunk'] == group['description']:
					res['plan_qty'] = group['plan_qty']
					res['rate'] = group['rate']
					res['total'] = group['total']
	return result

def get_columns(filters):
	columns = [
		{
			'fieldname': 'trunk',
			'label': _('Description'),
			'fieldtype': 'Data',
			'width': 300,
			'align': 'left'
		},
		{
			'fieldname': 'stock_qty',
			'label': _('Stock Qty'),
			'fieldtype': 'Float',
			'width': 100,
		},
		{
			'fieldname': 'plan_qty',
			'label': _('Plan Qty'),
			'fieldtype': 'Float',
			'width': 100
		},
		{
			'fieldname': 'unit',
			'label': _('Unit'),
			'fieldtype': 'Link',
			'options': 'UOM',
			'width': 100
		},
		{
			'fieldname': 'rate',
			'label': _('Rate'),
			'fieldtype': 'Currency',
			'width': 100
		},
		{
			'fieldname': 'total',
			'label': _('Total'),
			'fieldtype': 'Currency',
			'width': 100
		},
		
	]
	return columns


@frappe.whitelist()
def get_quantity(item_code, company):
	sql = f"""
		SELECT
			sum(ledger.actual_qty) as actual_qty
   		FROM
			`tabBin` AS ledger
   			INNER JOIN `tabItem` AS item    ON ledger.item_code = item.item_code
   			INNER JOIN `tabWarehouse` as warehouse    ON warehouse.name = ledger.warehouse
   		WHERE
			ledger.item_code = "{item_code}" AND
			warehouse.company = "{company}"

		"""
	actual_quantity = frappe.db.sql(f"{sql}", as_dict=True)
	return actual_quantity







def get_group_qty(item_group,company):
	actual_qty = frappe.db.sql(
			"""
			SELECT sum(actual_qty) as qty,item_code,warehouse 
			FROM `tabBin` b
			LEFT JOIN (SELECT name,item_group from `tabItem`) as i ON b.item_code = i.name
			LEFT JOIN (SELECT name,company from `tabWarehouse`) as w ON b.warehouse = w.name
			WHERE i.item_group = '%s' and w.company = "%s"
			""" %(item_group,company),as_dict=True)


	return actual_qty[0]['qty']