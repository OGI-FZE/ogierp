# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from oil_and_gas_international.overriding import get_income_expense_accounts

class RentalInvoice(Document):
	def validate(self):
		for row in self.items:
			row.income_account = get_income_expense_accounts(row.item_code,self.company)[0]
			row.expense_account = get_income_expense_accounts(row.item_code,self.company)[1]

		if self.taxes_and_charges:
			self.tax_amount = self.taxes[0].tax_amount
			self.grand_total = self.tax_amount + self.total
		else:
			self.grand_total = self.total



		
