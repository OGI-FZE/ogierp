# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	if filters.get('group_by') == 'country':
		columns = [
			{
				'label':_('Country'),
				'field_name':'group_by',
				'fieldtype':'Link',
				'options':'Country',
				'width':200
			}
		]

	if filters.get('group_by') == 'customer':
		columns = [
			{
				'label':_('Customer'),
				'field_name':'group_by',
				'fieldtype':'Link',
				'options':'Customer',
				'width':200
			}
		]

	if filters.get('group_by') == 'sales_person':
		columns = [
			{
				'label':_('Sales Person'),
				'field_name':'group_by',
				'fieldtype':'Link',
				'options':'Sales Person',
				'width':200
			}
		]

	if filters.get('group_by') == 'item_group':
		columns = [
			{
				'label':_('Product Main Group'),
				'field_name':'group_by',
				'fieldtype':'Link',
				'options':'Item Group',
				'width':200
			}
		]

	if filters.get('group_by') == 'division':
		columns = [
			{
				'label':_('Division'),
				'field_name':'group_by',
				'fieldtype':'Data',
				'width':200
			}
		]

	month_list = ["january","february","march","april","may","june","july","august","september","october","november","december"]

	for m in month_list:
		columns += ([
				{
					'label': m[:3]+filters.get("fiscal_year"),
					'field_name':m+filters.get("fiscal_year"),
					'fieldtype':'Currency',
					'width':100
				}
			])

	return columns

def get_data(filters):
	data = []
	# data=[{'country':'India','jan2022': 100,'feb2022': 100,'mar2022': 100,'apr2022': 100,'may2022': 100,'jun2022': 100,
	# 'jul2022': 100,'aug2022': 100,'sep2022': 100,'oct2022': 100,'nov2022': 100,'dec2022': 100}]

	forecast_doc = frappe.get_list("Forecast Document",fields=["name","version"],filters={'fiscal_year':filters.get('fiscal_year'),'company':filters.get('company'),'docstatus':1},order_by='version')
	if forecast_doc:
		latest = forecast_doc[-1]['name']

		data = frappe.db.sql("""select tft.{0} as group_by,sum(tft.january) as jan{1},sum(tft.february) as feb{1},sum(tft.march) as mar{1},
				sum(tft.april) as apr{1},sum(tft.may) as may{1},sum(tft.june) as jun{1},sum(tft.july) as jul{1},sum(tft.august) as aug{1}
				,sum(tft.september) as sep{1},sum(tft.october) as oct{1},sum(tft.november) as nov{1},sum(tft.december) as dec{1} from `tabForecast target` tft 
				WHERE tft.parent='{2}' and tft.{0}!='' and tft.docstatus = 1 group by tft.{0}""".format(filters.get('group_by'),filters.get('fiscal_year'),latest))

		print("\ndata\n",data)

		# frappe.db.sql("""select tft.%s as group_by,sum(tft.january) as jan2022,sum(tft.february) as feb2022,sum(tft.march) as mar2022,
		# 	sum(tft.april) as apr2022,sum(tft.may) as may2022,sum(tft.june) as jun2022,sum(tft.july) as jul2022,sum(tft.august) as aug2022
		# 	,sum(tft.september) as sep2022,sum(tft.october) as oct2022,sum(tft.november) as nov2022,sum(tft.december) as dec2022 from `tabForecast target` tft 
		# 	WHERE tft.parent='%s' and %s is not null and tft.docstatus = 1 group by %s"""%(filters.get('group_by'),latest,filters.get('group_by'),filters.get('group_by')))
	else:
		frappe.throw("Please create a forecast document for selected fiscal year")
	
	return data

