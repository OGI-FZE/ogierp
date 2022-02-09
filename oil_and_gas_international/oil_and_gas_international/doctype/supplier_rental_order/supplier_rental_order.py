# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SupplierRentalOrder(Document):
	def on_submit(self):
		if self.supplier_rental_quotation:
			self.status = "Open"
			frappe.set_value("Supplier Rental Quotation", self.supplier_rental_quotation, "status", "Ordered")
		frappe.db.commit()

	@frappe.whitelist()
	def get_supplier_rental_quotation_items(docname=None):
		if not docname:
			return {}

		doc = frappe.get_doc("Supplier Rental Quotation", docname)
		response = {
			"name": doc.name,
			"supplier":	doc.supplier,
			"date":	doc.date,
			"rate_type": doc.rate_type,
			"rq_items":	doc.items,
		}

		return response
