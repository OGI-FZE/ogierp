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
		# self.get_chart_data()

		# Skipping total row for tree-view reports
		skip_total_row = 0

		if self.filters.tree_type in ["Product Main Group"]:
			skip_total_row = 1

		return self.columns, self.data, None, None, skip_total_row

	def get_columns(self):
		self.columns = [
			{
				"label": _(self.filters.tree_type),
				"options": self.filters.tree_type if self.filters.tree_type != "Division" else "",
				"fieldname": "entity",
				"fieldtype": "Link" if self.filters.tree_type != "Division" else "Data",
				"width": 140 if self.filters.tree_type != "Division" else 200,
			}
		]


		for end_date in self.periodic_daterange:
			period = self.get_period(end_date)
			self.columns.append(
					{"label": _(period), "fieldname": scrub(period), "fieldtype": "Float", "width": 120}
				)
			for pp in ["SO","SI"]:
				self.columns.append(
					{"label": pp + " " +_(period), "fieldname": scrub(pp + " " +period), "fieldtype": "Float", "width": 120}
				)

	def get_data(self):
		if self.filters.tree_type == "Customer":
			self.get_sales_transactions_based_on_customers()
			self.get_rows()

		elif self.filters.tree_type == "Country":
			self.get_sales_transactions_based_on_country()
			self.get_rows()

		elif self.filters.tree_type == "Division":
			self.get_sales_transactions_based_on_division()
			self.get_rows()

		elif self.filters.tree_type == "Sales Person":
			self.get_sales_transactions_based_on_sp()
			self.get_rows()

		elif self.filters.tree_type == "Item Group":
			self.get_sales_transactions_based_on_item_group()
			self.get_rows()


	def get_sales_transactions_based_on_customers(self):
		value_field = "base_net_total as value_field"
		entity = "customer as entity"

		self.so_entries = frappe.get_all(
			"Sales Order",
			fields=[entity, value_field, "transaction_date"],
			filters={
				"docstatus": 1,
				"company": self.filters.company,
				"transaction_date": ("between", [frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")]),
			},
		)

		self.si_entries = frappe.get_all(
			"Sales Invoice",
			fields=[entity, value_field, "posting_date"],
			filters={
				"docstatus": 1,
				"company": self.filters.company,
				"posting_date": ("between", [frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")]),
			},
		)

	def get_sales_transactions_based_on_division(self):
		value_field = "base_net_total as value_field"

		entity = "departments as entity"

		self.so_entries = frappe.get_all(
			"Sales Order",
			fields=[entity, value_field, "transaction_date"],
			filters={
				"docstatus": 1,
				"company": self.filters.company,
				"departments":['!=',''],
				"transaction_date": ("between", [frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")]),
			},
		)

		self.si_entries = frappe.get_all(
			"Sales Invoice",
			fields=[entity, value_field, "posting_date"],
			filters={
				"docstatus": 1,
				"company": self.filters.company,
				"departments":['!=',''],
				"posting_date": ("between", [frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")]),
			},
		)

	def get_sales_transactions_based_on_country(self):
		value_field = "base_net_total as value_field"

		entity = "territory as entity"

		self.so_entries = frappe.get_all(
			"Sales Order",
			fields=[entity, value_field, "transaction_date"],
			filters={
				"docstatus": 1,
				"company": self.filters.company,
				"departments":['!=',''],
				"transaction_date": ("between", [frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")]),
			},
		)

		self.si_entries = frappe.get_all(
			"Sales Invoice",
			fields=[entity, value_field, "posting_date"],
			filters={
				"docstatus": 1,
				"company": self.filters.company,
				"departments":['!=',''],
				"posting_date": ("between", [frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")]),
			},
		)


	def get_sales_transactions_based_on_item_group(self):
		value_field = "base_amount"

		self.so_entries = frappe.db.sql(
			"""
			select i.item_group as entity, i.{value_field} as value_field, s.transaction_date
			from `tabSales Order Item` i , `tabSales Order` s
			where s.name = i.parent and s.docstatus = 1 and s.company = %s
			and s.transaction_date between %s and %s
		""".format(
				value_field=value_field
			),
			(self.filters.company, frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")),
			as_dict=1,
		)

		self.si_entries = frappe.db.sql(
			"""
			select i.item_group as entity, i.{value_field} as value_field, s.posting_date
			from `tabSales Invoice Item` i , `tabSales Invoice` s
			where s.name = i.parent and s.docstatus = 1 and s.company = %s
			and s.posting_date between %s and %s
		""".format(
				value_field=value_field
			),
			(self.filters.company, frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")),
			as_dict=1,
		)

	def get_sales_transactions_based_on_sp(self):
		value_field = "base_net_total"

		self.so_entries = frappe.db.sql(
			"""
			select i.sales_person as entity, s.{value_field} as value_field, s.transaction_date
			from `tabSales Team` i , `tabSales Order` s
			where s.name = i.parent and s.docstatus = 1 and s.company = %s and i.sales_person !=''
			and s.transaction_date between %s and %s
		""".format(
				value_field=value_field
			),
			(self.filters.company, frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")),
			as_dict=1,
		)

		self.si_entries = frappe.db.sql(
			"""
			select i.sales_person as entity, s.{value_field} as value_field, s.posting_date
			from `tabSales Team` i , `tabSales Invoice` s
			where s.name = i.parent and s.docstatus = 1 and s.company = %s and i.sales_person !=''
			and s.posting_date between %s and %s
		""".format(
				value_field=value_field
			),
			(self.filters.company, frappe.defaults.get_user_default("year_start_date"), frappe.defaults.get_user_default("year_end_date")),
			as_dict=1,
		)

	def get_rows(self):
		self.data = []
		self.get_periodic_data()
		self.forecast_data = frappe._dict()
		self.forecast_entries = frappe._dict()

		value_field = "base_net_total as value_field"

		if self.filters.tree_type == "Customer":
			entity = "customer"
		elif self.filters.tree_type == "Division":
			entity = "division"
		elif self.filters.tree_type == "Item Group":
			entity = "item_group"
		elif self.filters.tree_type == "Country":
			entity = "country"
		elif self.filters.tree_type == "Sales Person":
			entity = "sales_person"

		self.get_forecast_entries()

		def combine_dict(d1, d2):
		    return {
		        k: list(d[k] for d in (d1, d2) if k in d)
		        for k in set(d1.keys()) | set(d2.keys())
		    }

		self.entity_periodic_data = combine_dict(self.so_periodic_data,self.si_periodic_data)
		for t in self.entity_periodic_data:
			self.entity_periodic_data[t] = reduce(lambda a, b: dict(a, **b), self.entity_periodic_data[t])
				
		for entity, period_data in iteritems(self.entity_periodic_data):
			row = {
				"entity": entity,
			}
			for end_date in self.periodic_daterange:
				so_period = self.get_period_so(end_date)
				so_amount = flt(period_data.get(so_period, 0.0))
				row[scrub(so_period)] = so_amount

				si_period = self.get_period_si(end_date)
				si_amount = flt(period_data.get(si_period, 0.0))
				row[scrub(si_period)] = si_amount

			
			for d in self.forecast_data:
				if d["entity"] == row["entity"]:
					for k,v in d.items():
						if k!='entity':
							row[k] = v

			if self.filters.range == "Monthly":
				for m in self.months:
					all_forecasted = m.lower() + "_" + self.filters.fiscal_year
					if all_forecasted not in row.keys():
						row.setdefault(all_forecasted, 0.0)

			if self.filters.range == "Quarterly":
				for m in ['quarter_1','quarter_2','quarter_3','quarter_4']:
					all_forecasted = m + "_" + self.filters.fiscal_year
					if all_forecasted not in row.keys():
						row.setdefault(all_forecasted, 0.0)

			if self.filters.range == "Yearly":
				if self.filters.fiscal_year not in row.keys():
					row.setdefault(self.filters.fiscal_year, 0.0)



			self.data.append(row)

	def get_periodic_data(self):
		# self.entity_periodic_data = frappe._dict()
		self.so_periodic_data = frappe._dict()
		self.si_periodic_data = frappe._dict()
		
		for so in self.so_entries:
			period = self.get_period_so(so.get("transaction_date"))
			self.so_periodic_data.setdefault(so.entity, frappe._dict()).setdefault(period, 0.0)
			self.so_periodic_data[so.entity][period] += flt(so.value_field)

		for si in self.si_entries:
			period = self.get_period_si(si.get("posting_date"))
			self.si_periodic_data.setdefault(si.entity, frappe._dict()).setdefault(period, 0.0)
			self.si_periodic_data[si.entity][period] += flt(si.value_field)

	def get_forecast_entries(self):
		if self.filters.tree_type == "Customer":
			entity = "customer"
		elif self.filters.tree_type == "Division":
			entity = "division"
		elif self.filters.tree_type == "Item Group":
			entity = "item_group"
		elif self.filters.tree_type == "Country":
			entity = "country"
		elif self.filters.tree_type == "Sales Person":
			entity = "sales_person"

		forecast_doc = frappe.get_list("Forecast Document",fields=["name","version"],
			filters={'fiscal_year':self.filters.fiscal_year,'company':self.filters.company},order_by='version')

		if forecast_doc:
			latest = forecast_doc[-1]['name']

			if self.filters.range == "Monthly":
				self.forecast_entries = frappe.db.sql("""select tft.{0} as entity,sum(tft.january) as jan_{1},sum(tft.february) as feb_{1},sum(tft.march) as mar_{1},
					sum(tft.april) as apr_{1},sum(tft.may) as may_{1},sum(tft.june) as jun_{1},sum(tft.july) as jul_{1},sum(tft.august) as aug_{1}
					,sum(tft.september) as sep_{1},sum(tft.october) as oct_{1},sum(tft.november) as nov_{1},sum(tft.december) as dec_{1} from `tabForecast target` tft 
					WHERE tft.parent='{2}' and tft.{0}!='' and tft.docstatus = 1 group by tft.{0}""".format(entity,self.filters.fiscal_year,latest),as_dict=1)
				if self.forecast_entries: 
					self.forecast_data = self.forecast_entries
			
			if self.filters.range == "Quarterly":
				self.forecast_entries = frappe.db.sql("""select tft.{0} as entity,sum(tft.january)+sum(tft.february)+sum(tft.march) as quarter_1_{1},
					sum(tft.april)+sum(tft.may)+sum(tft.june) as quarter_2_{1},sum(tft.july)+sum(tft.august)+sum(tft.september) as quarter_3_{1},sum(tft.october)+sum(tft.november)+sum(tft.december) as quarter_4_{1} 
					from `tabForecast target` tft 
					WHERE tft.parent='{2}' and tft.{0}!='' and tft.docstatus = 1 group by tft.{0}""".format(entity,self.filters.fiscal_year,latest),as_dict=1)
				if self.forecast_entries: 
					self.forecast_data = self.forecast_entries

			if self.filters.range == "Yearly":
				self.forecast_entries = frappe.db.sql("""select tft.{0} as entity,sum(tft.january)+sum(tft.february)+sum(tft.march)+sum(tft.april)+sum(tft.may)+sum(tft.june)+sum(tft.july)+sum(tft.august)+sum(tft.september)+sum(tft.october)+sum(tft.november)+sum(tft.december) as '{1}' 
					from `tabForecast target` tft 
					WHERE tft.parent='{2}' and tft.{0}!='' and tft.docstatus = 1 group by tft.{0}""".format(entity,self.filters.fiscal_year,latest),as_dict=1)
				if self.forecast_entries: 
					self.forecast_data = self.forecast_entries

	def get_period(self, posting_date):
		if self.filters.range == "Monthly":
			period = str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)
		elif self.filters.range == "Quarterly":
			period = "Quarter " + str(((posting_date.month - 1) // 3) + 1) + " " + str(posting_date.year)
		else:
			year = get_fiscal_year(posting_date, company=self.filters.company)
			period = str(year[0])
		return period

	def get_period_so(self, posting_date):
		if self.filters.range == "Monthly":
			period = "SO" + " " + str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)
		elif self.filters.range == "Quarterly":
			period = "SO" + " " + "Quarter " + str(((posting_date.month - 1) // 3) + 1) + " " + str(posting_date.year)
		else:
			year = get_fiscal_year(posting_date, company=self.filters.company)
			period = "SO" + " " + str(year[0])
		return period

	def get_period_si(self, posting_date):
		if self.filters.range == "Monthly":
			period = "SI" + " " + str(self.months[posting_date.month - 1]) + " " + str(posting_date.year)
		elif self.filters.range == "Quarterly":
			period = "SI" + " " + "Quarter " + str(((posting_date.month - 1) // 3) + 1) + " " + str(posting_date.year)
		else:
			year = get_fiscal_year(posting_date, company=self.filters.company)
			period = "SI" + " " + str(year[0])
		return period

	def get_period_date_ranges(self):
		from dateutil.relativedelta import MO, relativedelta

		from_date, to_date = getdate(frappe.defaults.get_user_default("year_start_date")), getdate(frappe.defaults.get_user_default("year_end_date"))

		increment = {"Monthly": 1, "Quarterly": 3, "Half-Yearly": 6, "Yearly": 12}.get(
			self.filters.range, 1
		)

		if self.filters.range in ["Monthly", "Quarterly"]:
			from_date = from_date.replace(day=1)
		elif self.filters.range == "Yearly":
			from_date = get_fiscal_year(from_date)[1]
		else:
			from_date = from_date + relativedelta(from_date, weekday=MO(-1))

		self.periodic_daterange = []
		for dummy in range(1, 53):
			period_end_date = add_to_date(from_date, months=increment, days=-1)

			if period_end_date > to_date:
				period_end_date = to_date

			self.periodic_daterange.append(period_end_date)

			from_date = add_days(period_end_date, 1)
			if period_end_date == to_date:
				break