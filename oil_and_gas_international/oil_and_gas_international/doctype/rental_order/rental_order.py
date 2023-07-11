# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.accounts_controller import get_taxes_and_charges


class RentalOrder(Document):
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
        
    def on_submit(self):
        if self.start_date and not self.end_date:
            self.db_set("status","On Rent")
 


        if self.rental_quotation:
            frappe.set_value("Rental Quotation",
                             self.rental_quotation, "status", "Ordered")
        # self.db_set("status", "Submitted")
        pro = frappe.new_doc("Project")
        pro.project_name = self.name
        pro.company = self.company
        pro.department = self.department
        pro.rental_order = self.name
        pro.expected_start_date = self.date
        pro.customer = self.customer
        pro.division = self.division
        pro.project_type = 'External'
        pro.save()
        frappe.db.commit()
    def on_cancel(self):
        self.db_set("status", "Cancelled")

@frappe.whitelist()
def get_rental_quotation_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Rental Quotation", docname)
    response = {
        "name": doc.name,
        "customer":	doc.customer,
        "date":	doc.date,
        "rate_type": doc.rate_type,
        "rq_items":	doc.items,
    }

    return response

@frappe.whitelist()
def get_taxes(ro=None,tt=None):
    ro_doc = frappe.get_doc("Rental Order",ro)
    if tt and not ro_doc.get('taxes'):
        taxes = get_taxes_and_charges('Sales Taxes and Charges Template', tt)
        if taxes:
            return taxes

def set_status():
    ro_docs = frappe.get_list("Rental Issue Note",fields=["name","docstatus"])
    for row in ro_docs:
        if row.docstatus == 1:
            frappe.set_value("Rental Issue Note", row.name, "status", "Submitted")
        if row.docstatus == 2:
            frappe.db.sql("""update `tabRental Issue Note` tro set tro.status='Cancelled' where tro.name='{0}'""".format(row.name))
            # frappe.set_value("Rental Order", row.name, "status", "Cancelled")
    frappe.db.commit()

@frappe.whitelist()
def get_transfered_qty(ro=None):
    doc = frappe.get_doc("Rental Order", ro)
    data = []
    for item in doc.items:
        data.append({'item_code':item.item_code,'qty':item.transfered_qty})
    return data
        