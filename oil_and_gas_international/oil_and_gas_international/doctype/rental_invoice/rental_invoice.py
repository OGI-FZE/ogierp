# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class RentalInvoice(Document):
	def validate(self):
		
		if self.taxes_and_charges:
			self.tax_amount = self.taxes[0].tax_amount
			self.grand_total = self.tax_amount + self.total
		else:
			self.grand_total = self.total


		
