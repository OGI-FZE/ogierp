# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff,today

def execute(filters=None):
	columns = [
		{
			"label": "Asset",
			"fieldtype": "Link",
			"options":"Asset",
			"fieldname": "asset",
			"width": 100
		},
		{
			"label": "Asset Name",
			"fieldtype": "Data",
			"fieldname": "asset_name",
			"width": 150
		},
		{
			"label": "Life",
			"fieldtype": "Int",
			"fieldname": "life",
			"width": 80
		},
		{
			"label": "Operational/Running",
			"fieldtype": "Int",
			"fieldname": "op",
			"width": 80
		},
		{
			"label": "Standby",
			"fieldtype": "Int",
			"fieldname": "standby",
			"width": 80
		},
		{
			"label": "Straight",
			"fieldtype": "Int",
			"fieldname": "straight",
			"width": 80
		},
		{
			"label": "Utilization",
			"fieldtype": "Int",
			"fieldname": "utilization",
			"width": 80
		},
		{
			"label": "Revenue",
			"fieldtype": "Float",
			"fieldname": "revenue",
			"width": 80
		},
		{
			"label": "Supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"fieldname": "supplier",
			"width": 170
		},
		{
			"label": "Purchase Date",
			"fieldtype": "Date",
			"fieldname": "pur_date",
			"width": 100,
		},
		{
			"label": "Gross Purchase Rate",
			"fieldtype": "Float",
			"fieldname": "gross_rate",
			"width": 100,
		},
	]

	data = get_data(filters)
	return columns, data

def get_data(filters):
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
	data = []

	print("<<<<<<<<<<>>>>>>>>>>>>>>>>>>",frappe.db.sql("""DECLARE @count INT;
		SET @count = 1;
		    
		WHILE @count<= 5
		BEGIN
		   PRINT @count
		   SET @count = @count + 1;
		END;"""))

	# rt = frappe.db.sql("""select trt.name,trt.date,trt.customer,trt.start_date ,trt.end_date,trti.assets,
	# 		sum(trti.operational_running_days) as 'total_op_days',trti.operational_running as 'op_rate', sum(CASE WHEN trti.operational_running_days  > 0 THEN (trti.operational_running*trti.operational_running_days) ELSE 0 END) as 'total_op_amnt',
	# 		sum(trti.standby_days) as 'total_sb_days',trti.standby as 'sb_rate',sum(CASE WHEN trti.standby_days  > 0 THEN (trti.standby*trti.standby_days) ELSE 0 END) as 'total_sb_amnt',
	# 		sum(trti.straight_days) as 'total_str_days',trti.straight_days as 'str_rate',sum(CASE WHEN trti.straight_days  > 0 THEN (trti.straight*trti.straight_days) ELSE 0 END) as 'total_str_amnt',
	# 		sum(trti.amount) as 'total_amount'
	# 		from `tabRental Timesheet` trt 
	# 		join `tabRental Timesheet Item` trti 
	# 		on trti.parent = trt.name 
	# 		where trt.docstatus =1 and (trti.assets = '{0}' or trti.assets = '{0}\n')
	# 		group by trt.name""".format(filters.get('asset')),as_dict=True)
	

	# if not rt:
	# 	return data

	# total_op = 0
	# total_sb = 0
	# total_st = 0
	# total_amnt = 0

	# for ts in rt:
	# 	total_amnt += (ts.total_op_amnt+ts.total_sb_amnt+ts.total_str_amnt)
	# 	row = {
	# 		'date':ts.date,
	# 		'timesheet':ts.name,
	# 		'customer':ts.customer,
	# 		'from_date':ts.start_date,
	# 		'to_date':ts.end_date,
	# 		'rental_status':"Operational/Running",
	# 		'days':ts.total_op_days,
	# 		'rental_rate':ts.op_rate,
	# 		'rental_amount':ts.total_op_amnt
	# 	}
	# 	total_op += ts.total_op_days

	# 	data.append(row)

	# 	row = {
	# 		'rental_status':"Standby",
	# 		'days':ts.total_sb_days,
	# 		'rental_rate':ts.sb_rate,
	# 		'rental_amount':ts.total_sb_amnt
	# 	}
	# 	total_sb += ts.total_sb_days

	# 	data.append(row)

	# 	row = {
	# 		'rental_status':"Straight",
	# 		'days':ts.total_str_days,
	# 		'rental_rate':ts.str_rate,
	# 		'rental_amount':ts.total_str_amnt
	# 	}
	# 	total_st += ts.total_str_days

	# 	data.append(row)

	# data.append({})

	# row = {
	# 	'rental_status':'Total Operational Days',
	# 	'days': total_op,
	# }
	# data.append(row)

	# row = {
	# 	'rental_status':'Total Standby Days',
	# 	'days': total_sb,
	# }
	# data.append(row)

	# row = {
	# 	'rental_status':'Total Straight Days',
	# 	'days': total_st,
	# }
	# data.append(row)

	# asset_doc = frappe.get_doc("Asset",filters.get('asset'))
	# pur_date = asset_doc.purchase_date

	# row = {
	# 	'rental_status':'Total Life',
	# 	'days': date_diff(today(), pur_date),
	# }
	# data.append(row)

	# row = {
	# 	'rental_status':'Utilization',
	# 	'days': total_op+total_sb+total_st,
	# }
	# data.append(row)

	# row = {
	# 	'rental_status':'Revenue',
	# 	'days': total_amnt,
	# }
	# data.append(row)



	return data


