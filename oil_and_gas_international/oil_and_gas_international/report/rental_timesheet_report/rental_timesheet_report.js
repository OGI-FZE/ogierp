// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rental Timesheet Report"] = {
	"filters": [
		{
			'fieldname':'customer',
			'label':__('Customer'),
			'fieldtype':'Link',
			'options':'Customer',
			'width':100,
			},

	]
};

