from __future__ import unicode_literals
from frappe import _
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

@frappe.whitelist()
def make_proforma_invoice(source_name, target_doc=None):

	def update_status(source_doc, target_doc, source_parent):
		target_doc.status = "Draft"
		target_doc.sales_order = source_doc.name
	

	doclist = []
	doclist = get_mapped_doc("Sales Order", source_name, 	{
		"Sales Order": {
			"doctype": "Proforma Invoice",
			"field_map": {
				"company": "company",
				"delivery_date": "delivery_date",
				"advance_paid": "advance_paid",
			},
			"validation": {
				"docstatus": ["=", 1]
			},
			"postprocess": update_status,
		},
		"Sales Order Item": {
			"doctype": "Proforma Invoice Item",
			"field_map": {
				"item_code": "item_code",
				"delivery_date": "delivery_date",
			},
		},
	}, target_doc)

	return doclist