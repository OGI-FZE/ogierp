# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe import _
from frappe.model.document import Document
from itertools import groupby
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

class EstimationSheet(Document):
	pass


@frappe.whitelist()
def make_estimation(source_name, target_doc=None):
	doclist = get_mapped_doc("Opportunity", source_name, {
			"Opportunity": {
				"doctype": "Estimation Sheet",
				"field_map": {
					"name" : "opportunity"
				}
			},
			"Opportunity Item": {
				"doctype": "Estimation Sheet Item",
				"field_map": {
					"item_code": "item_code"
				},
			}
		}, target_doc)

	return doclist


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		from erpnext.controllers.accounts_controller import get_default_taxes_and_charges
		quotation = frappe.get_doc(target)

		company_currency = frappe.get_cached_value('Company',  quotation.company,  "default_currency")

		party_account_currency = company_currency

		quotation.currency = party_account_currency or company_currency

		if company_currency == quotation.currency:
			exchange_rate = 1
		else:
			exchange_rate = get_exchange_rate(quotation.currency, company_currency,
				quotation.transaction_date, args="for_selling")

		quotation.conversion_rate = exchange_rate

		# get default taxes
		taxes = get_default_taxes_and_charges("Sales Taxes and Charges Template", company=quotation.company)
		if taxes.get('taxes'):
			quotation.update(taxes)

		quotation.run_method("set_missing_values")
		quotation.run_method("calculate_taxes_and_totals")
		# if not source.with_items:
		quotation.opportunity = source.opportunity

	doclist = get_mapped_doc("Estimation Sheet", source_name, {
		"Estimation Sheet": {
			"doctype": "Quotation",
			"field_map": {
				"name": "against_estimation_sheet"
			}
		},
		"Estimation Sheet Item": {
			"doctype": "Quotation Item",
			"field_map": {
				'Opportunity': "prevdoc_docname",
				"opportunity": "prevdoc_doctype",
				"uom": "stock_uom",
				"unit_cost":"rate"
			},
			"add_if_empty": True,
			# "field_no_map": ['quotation_to']
		}
	}, target_doc, set_missing_values)

	return doclist

