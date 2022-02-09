# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SupplierRentalQuotation(Document):
	def on_cancel(self):
		self.status = "Canceled"

	def on_submit(self):
		self.status = "Open"
