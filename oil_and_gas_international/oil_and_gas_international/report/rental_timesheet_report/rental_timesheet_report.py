import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
  columns, data = [], []
  columns = get_columns(filters)
  data = get_data(filters)
  return columns, data

def get_data(filters):
	query = f'''
				SELECT
				rt.project as project,
				rt.name as rental_timesheet,
				rt.customer as customer,
				pii.item_code as item_description,
				pii.qty as qty,
				pii.start_date_ as rental_start_date,
				CASE WHEN pii.stop_rent = 1 THEN pii.end_date ELSE " " END AS rental_end_date,
				pii.rate as daily_rental_rate,
				pii.rate*pii.qty as daily_rental_total,
				srt.supplier as supplier,
				st.rate as sub_rental_rate,
				pii.qty*st.rate as sub_rental_total,
				(pii.rate*pii.qty)-(pii.qty*st.rate) as gp,
				pii.days as rental_days,
				st.days as sub_rental_days,
				pii.rate*pii.qty*pii.days as rental_revenue

				FROM
				`tabRental Timesheet` AS rt LEFT JOIN
				`tabProforma Invoice Item` AS pii ON
				pii.parent = rt.name,
				`tabSupplier Rental Timesheet` AS srt LEFT JOIN
				`tabSubrent Timesheet` AS st ON
				st.parent = srt.name
				WHERE
				rt.docstatus != 2 AND rt.rental_order = srt.rental_order AND
				srt.docstatus != 2 AND rt.end_date = srt.end_date AND 
				rt.project = srt.project AND pii.item_code = st.item_code
				'''

	data= frappe.db.sql(f"{query}", as_dict=True)
	for record in put_missed_sub_rental_timesheet_items()['subrental_additional']:
		data.append(record)
	for record in put_missed_sub_rental_timesheet_items()['rental_timesheet_additional']:
		data.append(record)

	data_filtered = data
	if filters.customer:
		counter = 0
		while counter < len(data):
			if data[counter]['customer'] != filters.customer:
				data_filtered = data.remove(data[counter])
			counter +=1	

	data.sort(key = lambda x:x['rental_start_date'])
	return data_filtered

def get_columns(filters):
  columns = [
	{'fieldname': 'project','label': _('Project'),'fieldtype': 'Link','options':'Project','width': 150},
	{'fieldname': 'rental_timesheet','label': _('Rental Timesheet'),'fieldtype': 'Link','options':'Rental Timesheet','width': 150},

	{'fieldname': 'customer','label': _('Customer'),'fieldtype': 'Link','options':'Customer','width': 150},
	{'fieldname': 'item_description','label': _('Item Description'),'fieldtype': 'Link','options':'Item','width': 150},
	{'fieldname': 'qty','label': _('Quantity'),'fieldtype': 'Data','width': 150},
	{'fieldname': 'rental_start_date','label': _('Rental Start Date'),'fieldtype': 'Date','width': 150},
	{'fieldname': 'rental_end_date','label': _('Rental End Date'),'fieldtype': 'Date','width': 150},
	{'fieldname': 'daily_rental_rate','label': _('Daily Rental Rate'),'fieldtype': 'float','width': 150},
	{'fieldname': 'daily_rental_total','label': _('Daily Rental Total'),'fieldtype': 'float','width': 150},
	{'fieldname': 'supplier','label': _('Supplier'),'fieldtype': 'Link','options':'Supplier','width': 150},
	{'fieldname': 'sub_rental_rate','label': _('Sub Rental Rate'),'fieldtype': 'float','width': 150},
	{'fieldname': 'sub_rental_total','label': _('Sub Rental Total'),'fieldtype': 'float','width': 150},
	{'fieldname': 'gp','label': _('GP'),'fieldtype': 'float','width': 150},
	{'fieldname': 'rental_days','label': _('No of days (Rental)'),'fieldtype': 'float','width': 150},
	{'fieldname': 'sub_rental_days','label': _('No of days (Sub Rental)'),'fieldtype': 'float','width': 150},
	{'fieldname': 'rental_revenue','label': _('Rental revenue'),'fieldtype': 'Data','width': 150},
  ]
  return columns




def put_missed_sub_rental_timesheet_items():
	rental_order = frappe.db.sql("""select name from `tabRental Order`""",as_dict=1)
	ro_list = []
	subrental_additional = []
	rental_timesheet_additional = []
	for ro in rental_order:
		ro_list.append(ro['name'])
	for ro in ro_list:
		rental_timesheet = frappe.db.get_list("Rental Timesheet",{"rental_order":ro},pluck='name')
		for rt in rental_timesheet:
			rental_t = frappe.get_doc("Rental Timesheet", rt)
			end_date_str = frappe.db.get_value("Rental Timesheet",rt,"end_date")
			if not frappe.db.exists("Supplier Rental Timesheet",{"rental_order":ro,"end_date":end_date_str}):
				for item in rental_t.items:
								
					additionnal_data =  {
									"project": rental_t.project,
									"rental_timesheet": rental_t.name,
									"customer":rental_t.customer,
									"item_description": item.item_code,
									"qty": item.qty,
									"rental_start_date": item.start_date_,
									"rental_end_date": " ",
									"daily_rental_rate": item.rate,
									"daily_rental_total": item.rate * item.qty,
									"supplier": " ",
									"sub_rental_rate": " ",
									"sub_rental_total": " ",
									"gp": item.rate*item.qty,
									"rental_days": item.days,
									"sub_rental_days": " ",
									"rental_revenue": item.rate*item.qty*item.days
					}
					subrental_additional.append(additionnal_data)
			else:
				supplier_rt = frappe.get_doc("Supplier Rental Timesheet",{"rental_order":ro,"end_date":end_date_str})
				for item in rental_t.items:
					for sitem in supplier_rt.items:
						if not sitem.item_code == item.item_code:
							print(rental_t)
							print(item.item_code)
							additionnal_data =  {
											"project": rental_t.project,
											"rental_timesheet": rental_t.name,
											"customer":rental_t.customer,
											"item_description": item.item_code,
											"qty": item.qty,
											"rental_start_date": item.start_date_,
											"rental_end_date": " ",
											"daily_rental_rate": item.rate,
											"daily_rental_total": item.rate * item.qty,
											"supplier": " ",
											"sub_rental_rate": " ",
											"sub_rental_total": " ",
											"gp": item.rate*item.qty,
											"rental_days": item.days,
											"sub_rental_days": " ",
											"rental_revenue": item.rate*item.qty*item.days

							}
							rental_timesheet_additional.append(additionnal_data)


	return {'subrental_additional':subrental_additional,'rental_timesheet_additional':rental_timesheet_additional}

