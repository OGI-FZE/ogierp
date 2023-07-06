# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe


class ProformaInvoice(Document):
	pass
# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from oil_and_gas_international.overriding import get_income_expense_accounts

class ProformaInvoice(Document):

    def before_save(self):
        total = 0
        qty = 0
        for row in self.items:
            row.delivery_date = self.delivery_date
            if not row.amount:
                row.amount = 0 
            total += row.amount
            qty += row.qty
            row.income_account = get_income_expense_accounts(row.item_code,self.company)[0]
            row.expense_account = get_income_expense_accounts(row.item_code,self.company)[1]
        self.total = total
        self.total_quantity = qty
        if self.taxes_and_charges:
            tax_amount = self.total*self.taxes[0].rate/100
            self.grand_total = tax_amount + self.total
            self.taxes[0].tax_amount = tax_amount
            self.taxes[0].total = self.grand_total
            self.tax_amount = tax_amount
        else:
            self.grand_total = self.total


    def validate(self):            
        pass
      



