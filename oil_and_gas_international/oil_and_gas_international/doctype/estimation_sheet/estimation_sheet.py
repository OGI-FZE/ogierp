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
