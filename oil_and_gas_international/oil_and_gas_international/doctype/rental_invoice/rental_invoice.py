# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from oil_and_gas_international.overriding import get_income_expense_accounts

class RentalInvoice(Document):
    def before_save(self):
        for row in self.items:
            row.delivery_date = self.from_date
    def validate(self):
        if self.customer:
            address = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Address' and link_name = '%s'"""% (self.customer), as_dict=1)  
            contact = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Contact' and link_name = '%s'"""% (self.customer), as_dict=1)  
            if address:
                cus_add = frappe.get_doc('Address',address[0]['parent'])
                if not self.customer_address:
                    self.customer_address = address[0]['parent']
                    self.address = cus_add.address_line1 + "\n" + cus_add.city + "\n" + cus_add.country
                else:
                    sec = frappe.get_doc('Address',self.customer_address)
                    self.address = sec.address_line1 + "\n" + sec.city + "\n" + sec.country
            if contact:
                cus_con = frappe.get_doc('Contact', contact[0]['parent'])
                if not self.customer_contact:
                    self.customer_contact = contact[0]['parent']
                    if cus_con.email_ids and cus_con.phone_nos:
                        self.contact = cus_con.phone_nos[0].phone + "\n" + cus_con.email_ids[0].email_id
                    elif cus_con.phone_nos:
                        self.contact = cus_con.phone_nos[0].phone
                    elif cus_con.email_ids:
                        self.contact = cus_con.email_ids[0].email_id
                else:
                    sec = frappe.get_doc('Contact',self.customer_contact)
                    if sec.email_ids and sec.phone_nos:
                        self.contact = sec.phone_nos[0].phone + "\n" + sec.email_ids[0].email_id
                    elif sec.phone_nos:
                        self.contact = sec.phone_nos[0].phone
                    elif sec.email_ids:
                        self.contact = sec.email_ids[0].email_id
        total = 0
        for row in self.items:
            if not row.amount:
                row.amount = 0 
            total += row.amount
            row.income_account = get_income_expense_accounts(row.item_code,self.company)[0]
            row.expense_account = get_income_expense_accounts(row.item_code,self.company)[1]
        self.total = total

        if self.taxes_and_charges:
            for row in self.items:
                row.tax_rate = self.taxes[0].rate
                row.tax_amount_ = (float(row.amount)*self.taxes[0].rate/100)
            self.tax_amount = self.taxes[0].tax_amount
            grand_total = self.tax_amount + self.total
            discount = self.additional_discount_percentage*float(grand_total)/100
            self.grand_total = grand_total - discount
        else:
            discount = self.additional_discount_percentage*float(total)/100
            self.grand_total = total - discount
            



        
