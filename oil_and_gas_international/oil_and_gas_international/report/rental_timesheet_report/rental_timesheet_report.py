import frappe
from frappe import _


def execute(filters=None):
  columns, data = [], []
  columns = get_columns(filters)
  data = get_data(filters)
  return columns, data

def get_data(filters):
	query = f'''
        SELECT
		  rt.project as project,
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
		  st.days as sub_rental_days

        FROM
          `tabRental Timesheet` AS rt LEFT JOIN
		  `tabProforma Invoice Item` AS pii ON
		  pii.parent = rt.name,
		  `tabSupplier Rental Timesheet` AS srt LEFT JOIN
		  `tabSubrent Timesheet` AS st ON
		  st.parent = srt.name
        WHERE
          rt.docstatus=1 AND rt.rental_order = srt.rental_order AND
		  srt.docstatus = 1 AND rt.end_date = srt.end_date AND
		  rt.project = srt.project AND pii.item_code = st.item_code
		'''
	if filters.customer:
		query = f"{query} AND rt.customer='{filters.customer}'"
	data= frappe.db.sql(f"{query}", as_dict=True)
	return data

def get_columns(filters):
  columns = [
	{
	  'fieldname': 'project',
	  'label': _('Project'),
	  'fieldtype': 'Link',
	  'options':'Project',
	  'width': 150
	},
	{
	  'fieldname': 'customer',
	  'label': _('Customer'),
	  'fieldtype': 'Link',
	  'options':'Customer',
	  'width': 150
	},
	{
	  'fieldname': 'item_description',
	  'label': _('Item Description'),
	  'fieldtype': 'Link',
	  'options':'Item',
	  'width': 150
	},
		{
	  'fieldname': 'qty',
	  'label': _('Quantity'),
	  'fieldtype': 'Data',
	  'width': 150
	},
	{
	  'fieldname': 'rental_start_date',
	  'label': _('Rental Start Date'),
	  'fieldtype': 'Date',
	  'width': 150
	},
		{
	  'fieldname': 'rental_end_date',
	  'label': _('Rental End Date'),
	  'fieldtype': 'Date',
	  'width': 150
	},
		{
	  'fieldname': 'daily_rental_rate',
	  'label': _('Daily Rental Rate'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'daily_rental_total',
	  'label': _('Daily Rental Total'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'supplier',
	  'label': _('Supplier'),
	  'fieldtype': 'Link',
	  'options':'Supplier',
	  'width': 150
	},
	{
	  'fieldname': 'sub_rental_rate',
	  'label': _('Sub Rental Rate'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'sub_rental_total',
	  'label': _('Sub Rental Total'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'gp',
	  'label': _('GP'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'rental_days',
	  'label': _('No of days (Rental)'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'sub_rental_days',
	  'label': _('No of days (Sub Rental)'),
	  'fieldtype': 'float',
	  'width': 150
	},
	{
	  'fieldname': 'rental_revenue',
	  'label': _('Rental revenue'),
	  'fieldtype': 'Data',
	  'width': 150
	},
  ]
  return columns