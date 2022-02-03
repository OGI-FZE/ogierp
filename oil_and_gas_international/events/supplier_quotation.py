from __future__ import unicode_literals
from frappe import _
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

@frappe.whitelist()
def make_purchase_requisition(source_name, target_doc=None):

	def update_status(source_doc, target_doc, source_parent):
		# target_doc.status = "Draft"
		target_doc.supplier_quotation = source_doc.name
	

	doclist = []
	doclist = get_mapped_doc("Supplier Quotation", source_name, 	{
		"Supplier Quotation": {
			"doctype": "Purchase Requisition",
			"field_map": {
				"company": "company",
			},
			"validation": {
				"docstatus": ["=", 1]
			},
			"postprocess": update_status,
		},
		"Supplier Quotation Item": {
			"doctype": "Purchase Requisition Item",
			"field_map": {
				"item_code": "item_code",
			},
		},
	}, target_doc)

	return doclist