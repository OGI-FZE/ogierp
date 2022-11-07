# Copyright (c) 2022, Craft
# For license information, please see license.txt

import frappe
from frappe import _, scrub
from frappe.utils import add_days, add_to_date, flt, getdate
from six import iteritems
from functools import reduce

from erpnext.accounts.utils import get_fiscal_year


def execute(filters=None):
	return Analytics(filters).run()


class Analytics(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		
		self.months = [
			"Jan",
			"Feb",
			"Mar",
			"Apr",
			"May",
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
			"Dec",
		]
		self.get_period_date_ranges()

	def run(self):
		self.get_columns()
		self.get_data()

		return self.columns, self.data, None, None

	def get_columns(self):
		self.columns = [
			{
				"label": 'Customer',
				"options": 'Customer',
				"fieldname": "customer",
				"fieldtype": "Link",
				"width":200
			},
			{
				"label": 'Country',
				"options": 'Country',
				"fieldname": "country",
				"fieldtype": "Link",
				"width":150
			},
			{
				"label": 'Sales Person',
				"options": 'Sales Person',
				"fieldname": "sales_person",
				"fieldtype": "Link",
				"width":150
			},
			{
				"label": 'Division',
				"options": 'Division',
				"fieldname": "division",
				"fieldtype": "Data",
				"width":150
			},
			{
				"label": 'Item Group',
				"options": 'Item Group',
				"fieldname": "item_group",
				"fieldtype": "Link",
				"width":150
			}
		]

		
		for end_date in self.periodic_daterange:
			period = str(self.months[end_date.month - 1]) + " " + str(end_date.year)
			self.columns.append(
					{"label": _(period), "fieldname": scrub(period), "fieldtype": "Float", "width": 120}
				)
			for pp in ["SO","SI"]:
				self.columns.append(
					{"label": pp + " " +_(period), "fieldname": scrub(pp + " " +period), "fieldtype": "Float", "width": 120}
				)	

	def get_data(self):
		self.data = []
		self.get_forecast_entries()
		self.get_sales_transactions_based_on_forecast()
		

		value_field = "base_net_total as value_field"

		def combine_dict(d1, d2):
		    return {
		        k: list(d[k] for d in (d1, d2) if k in d)
		        for k in set(d1.keys()) | set(d2.keys())
		    }

		# def combine_dict(d1, d2, d3):
		#     return {
		#         k: list(d[k] for d in (d1, d2, d3) if k in d)
		#         for k in set(d1.keys()) | set(d2.keys()) | set(d2.keys())
		#     }

		# self.entity_periodic_data = combine_dict(self.so_periodic_data,self.si_periodic_data,self.no_forecast_data)
		self.entity_periodic_data = combine_dict(self.so_periodic_data,self.si_periodic_data)
		for t in self.entity_periodic_data:
			self.entity_periodic_data[t] = reduce(lambda a, b: dict(a, **b), self.entity_periodic_data[t])

		# print("so\n\n",self.so_periodic_data)
		# print("si\n",self.si_periodic_data)
		# print("noforecast\n",self.no_forecast_data)
		# print("entity_periodic_data...........\n",self.entity_periodic_data)

		# self.entity_periodic_data.update(self.no_forecast_data)

		# print("entity_periodic_data...........\n",self.entity_periodic_data)

		for entity, period_data in iteritems(self.entity_periodic_data):
			i=0
			row = {}
			for index in ['customer','country','sales_person','division','item_group']:
				row.update({
					index: entity[i],
				})
				i +=1

			for d in self.forecast_data:
				if d["customer"] == row["customer"] and d["country"] == row["country"] and d["sales_person"] == row["sales_person"] and d["division"] == row["division"] and d["item_group"] == row["item_group"]:
					for k,v in d.items():
						if k not in ['customer','country','sales_person','division','item_group']:
							row[k] = v
				
			for end_date in self.periodic_daterange:
				so_period = self.get_period_so(end_date)
				so_amount = flt(period_data.get(so_period, 0.0))
				row[scrub(so_period)] = so_amount

				si_period = self.get_period_si(end_date)
				si_amount = flt(period_data.get(si_period, 0.0))
				row[scrub(si_period)] = si_amount

			for m in self.months:
				all_forecasted = m.lower() + "_" + self.filters.fiscal_year
				if all_forecasted not in row.keys():
					row.setdefault(all_forecasted, 0.0)

			self.data.append(row)
		# 	print("\nrow",row)
		# print("data",self.data)

		# self.data.append(self.no_forecast_data.copy())

		# print("data",self.data)

		# for r in self.no_forecast:
		# 	self.data.append(r)


	def get_sales_transactions_based_on_forecast(self):

		self.so_entries = []
		self.si_entries = []
		self.no_forecast = []

		def get_conditions(row):
			conditions = " and so.company = '{0}' ".format(self.filters.company)

			if(row.customer):
				conditions += " and so.customer = '{0}'".format(row.customer)

			if(row.country):
				conditions += " and so.territory = '{0}'".format(row.country)

			if(row.division):
				conditions += " and so.departments = '{0}'".format(row.division)

			if(row.item_group):
				conditions += " and soi.item_group = '{0}'".format(row.item_group)

			if(row.sales_person):
				conditions += " and st.sales_person = '{0}'".format(row.sales_person)


			return conditions

		for f_row in self.forecast_data:
			conditions = get_conditions(f_row)

			so_entries = frappe.db.sql("""
				select so.customer,so.departments as division,so.territory as country,soi.item_group,st.sales_person, so.base_net_total as value_field, so.transaction_date
				from `tabSales Order Item` soi , `tabSales Order` so
				left join `tabSales Team` st on so.name=st.parent 
				where so.name = soi.parent and so.docstatus = 1 and so.transaction_date between '{0}' and '{1}' {2}
				""".format(frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date"),conditions),as_dict=1)

			if so_entries:
				for so in so_entries:
					self.so_entries.append(so)

			si_entries = frappe.db.sql("""
				select so.customer,so.departments as division,so.territory as country,soi.item_group,st.sales_person, so.base_net_total as value_field, so.posting_date
				from `tabSales Invoice Item` soi , `tabSales Invoice` so
				left join `tabSales Team` st on so.name=st.parent 
				where so.name = soi.parent and so.docstatus = 1 and so.posting_date between '{0}' and '{1}' {2}
				""".format(frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date"),conditions),as_dict=1)

			if si_entries:
				for si in si_entries:
					self.si_entries.append(si)

			if not so_entries and not si_entries:
				self.no_forecast.append(f_row)



		# print("\n\nso_entries",so_entries)

		self.get_periodic_data()


	def get_periodic_data(self):
		self.so_periodic_data = frappe._dict()
		self.si_periodic_data = frappe._dict()
		self.no_forecast_data = frappe._dict()
		for so in self.so_entries:
			period = self.get_period_so(so.get("transaction_date"))
			self.so_periodic_data.setdefault((so.customer,so.country,so.sales_person,so.division,so.item_group), frappe._dict()).setdefault(period, 0.0)
			self.so_periodic_data[(so.customer,so.country,so.sales_person,so.division,so.item_group)][period] += flt(so.value_field)

		for si in self.si_entries:
			period = self.get_period_si(si.get("posting_date"))
			self.si_periodic_data.setdefault((si.customer,si.country,si.sales_person,si.division,si.item_group), frappe._dict()).setdefault(period, 0.0)
			self.si_periodic_data[(si.customer,si.country,si.sales_person,si.division,si.item_group)][period] += flt(si.value_field)

		for f in self.no_forecast:
			dic = frappe._dict()
			for m in self.months:
				dic['customer'] = f.customer
				dic['country'] = f.country
				dic['sales_person'] = f.sales_person
				dic['division'] = f.division
				dic['item_group'] = f.item_group
				so_no_forecasted = "so"+"_"+m.lower() + "_" + self.filters.fiscal_year
				si_no_forecasted = "si"+"_"+m.lower() + "_" + self.filters.fiscal_year
				m_no_forecasted = m.lower() + "_" + self.filters.fiscal_year

				dic[so_no_forecasted] = 0.00
				dic[si_no_forecasted] = 0.00
				dic.setdefault(m_no_forecasted, 0.0)
				dic[m_no_forecasted] += flt(f[m_no_forecasted])

			# print("///////self.no_forecast_data",dic)
			self.data.append(dic)

				# M_no_forecasted = m + " " + self.filters.fiscal_year
				# self.no_forecast_data.setdefault((f.customer,f.country,f.sales_person,f.division,f.item_group), frappe._dict()).setdefault(so_no_forecasted, 0.0)
				# self.no_forecast_data.setdefault((f.customer,f.country,f.sales_person,f.division,f.item_group), frappe._dict()).setdefault(si_no_forecasted, 0.0)
				# self.no_forecast_data.setdefault((f.customer,f.country,f.sales_person,f.division,f.item_group), frappe._dict()).setdefault(m_no_forecasted, 0.0)
				# self.no_forecast_data[(f.customer,f.country,f.sales_person,f.division,f.item_group)][m_no_forecasted] += flt(f[m_no_forecasted])


	def get_forecast_entries(self):
		self.forecast_data = frappe._dict()
		self.forecast_entries = frappe._dict()

		forecast_doc = frappe.get_list("Forecast Document",fields=["name","version"],
			filters={'fiscal_year':self.filters.fiscal_year,'company':self.filters.company},order_by='version')

		if forecast_doc:
			latest = forecast_doc[-1]['name']

			self.forecast_entries = frappe.db.sql("""select tft.customer,tft.country, tft.sales_person,tft.division,tft.item_group,tft.january as jan_{0},tft.february as feb_{0},tft.march as mar_{0},
				tft.april as apr_{0},tft.may as may_{0},tft.june as jun_{0},tft.july as jul_{0},tft.august as aug_{0}
				,tft.september as sep_{0},tft.october as oct_{0},tft.november as nov_{0},tft.december as dec_{0} from `tabForecast target` tft 
				WHERE tft.parent='{1}' and tft.docstatus = 1""".format(self.filters.fiscal_year,latest),as_dict=1)
			if self.forecast_entries: 
				self.forecast_data = self.forecast_entries


	def get_period_so(self, posting_date):
		period = "SO" + " " + str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)

		return period

	def get_period_si(self, posting_date):
		period = "SI" + " " + str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)
		
		return period

	def get_period_date_ranges(self):
		from dateutil.relativedelta import MO, relativedelta

		from_date, to_date = getdate(frappe.defaults.get_user_default("year_start_date")), getdate(frappe.defaults.get_user_default("year_end_date"))

		from_date = from_date.replace(day=1)

		self.periodic_daterange = []
		for dummy in range(1, 53):
			period_end_date = add_to_date(from_date, months=1, days=-1)

			if period_end_date > to_date:
				period_end_date = to_date

			self.periodic_daterange.append(period_end_date)

			from_date = add_days(period_end_date, 1)
			if period_end_date == to_date:
				break