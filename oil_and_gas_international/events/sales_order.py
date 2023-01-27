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

def create_project(doc, handler=None):
	project = frappe.new_doc("Project")
	if doc.division == 'Inspection':
		project.naming_series = 'OGI-.I-.MM.YY.-.####'
	elif doc.division == 'trading':
		project.naming_series = 'OGI-.TS-.MM.YY.-.####'
	elif doc.division == 'Machine Shop Repair':
	 	project.naming_series = 'OGI-.MS-.R-.MM.YY.-.###'
	project.customer = doc.customer
	project.project_name = project.naming_series
	project.sales_order = doc.name
	project.expected_start_date = doc.transaction_date
	project.division = doc.division
	project.save()
	frappe.db.commit()
# @frappe.whitelist()
# def get_weight(docname=None):
# 	print("\nvalidateeeee\n\n")
# 	doc = frappe.get_doc("Sales Order",docname)
# 	if(doc.docstatus==1 and doc.items):
# 		for i in doc.items:
# 			print(">>>>>>>>.weight",i.doctype,i.total_weight)
# 			print(">>>>>>>>.stock_qty*i.weight_per_unit",i.stock_qty,i.weight_per_unit)
# 			frappe.db.set_value(i.doctype, i.name, 'total_weight', (i.stock_qty*i.weight_per_unit));