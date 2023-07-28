// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Planning"] = {
	"filters": [
		{
			'fieldname':'company',
			'label':__('Company'),
			'fieldtype':'Link',
			'options':'Company',
			'width':100,
		},
		{
			'fieldname':'from_date',
			'label':__('From Date'),
			'fieldtype':'Date',
			'width':100,
		},
		{
			'fieldname':'to_date',
			'label':__('To Date'),
			'fieldtype':'Date',
			'width':100,
		},
		{
			'fieldname':'fiscal_year',
			'label':__('Fiscal Year'),
			'fieldtype':'Link',
			'options':'Fiscal Year',
			'width':100,
		},
	]
};