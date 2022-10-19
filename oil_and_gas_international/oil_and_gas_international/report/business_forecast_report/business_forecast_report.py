# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			'label':_('Country'),
			'field_name':'country',
			'fieldtype':'Link',
			'options':'Country',
			'width':200
		}
	]

	month_list = ["january","february","march","april","may","june","july","august","september","october","november","december"]

	for m in month_list:
		columns += ([
				{
					'label': m,
					'field_name':m+'forecast',
					'fieldtype':'Currency',
					'width':100
				},
				{
					'label': _('Invoiced'),
					'field_name':m+'invoiced',
					'fieldtype':'Currency',
					'width':100
				},
				{
					'label': _('Job Opened'),
					'field_name':m+'job_opened',
					'fieldtype':'Currency',
					'width':150
				},
			])

	return columns

def get_data(filters):

	

	data=[{'country':'India','januaryforecast': 100,'januaryinvoiced': 100,'januaryjob_opened': 100,'februaryforecast': 100,'februaryinvoiced': 100,'februaryjob_opened': 100,
	'marchforecast': 100,'marchinvoiced': 100,'marchjob_opened': 100,'aprilforecast': 100,'aprilinvoiced': 100,'apriljob_opened': 100,
	'mayforecast': 100,'mayinvoiced': 100,'mayjob_opened': 100,'juneforecast': 100,'juneinvoiced': 100,'junejob_opened': 100,
	'julyforecast': 100,'julyinvoiced': 100,'julyjob_opened': 100,'augustforecast': 100,'augustinvoiced': 100,'augustjob_opened': 100,
	'septemberforecast': 100,'septemberinvoiced': 100,'septemberjob_opened': 100,'octoberforecast': 100,'octoberinvoiced': 100,'octoberjob_opened': 100,
	'novemberforecast': 100,'novemberinvoiced': 100, 'novemberjob_opened': 100,'decemberforecast': 100,'decemberinvoiced': 100,'decemberjob_opened': 100}]
	
	return data

