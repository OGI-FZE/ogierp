# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentalQuotation(Document):
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
        elif self.lead:
            address = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Address' and link_name = '%s'"""% (self.lead), as_dict=1)  
            contact = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Contact' and link_name = '%s'"""% (self.lead), as_dict=1)  
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
                    else:
                        self.contact = cus_con.email_ids[0].email_id
                else:
                    sec = frappe.get_doc('Contact',self.customer_contact)
                    if sec.email_ids and sec.phone_nos:
                        self.contact = sec.phone_nos[0].phone + "\n" + sec.email_ids[0].email_id
                    elif sec.phone_nos:
                        self.contact = sec.phone_nos[0].phone
                    elif sec.email_ids:
                        self.contact = sec.email_ids[0].email_id
        rate_by_qty = []
        for row in self.items:
            if not row.operational_running:
                row.operational_running = 0
            rate_by_qty.append(row.qty*row.operational_running)
            total_rate_qty = sum(rate_by_qty)
        self.remarks = total_rate_qty*30
        print(self.total_by_month)
            
    def on_submit(self): 
        if self.rental_estimation:
            self.status = "Open"
            frappe.set_value("Rental Estimation",self.rental_estimation, "status", "To Quotation")
            frappe.db.commit()

    def on_cancel(self):
        self.status = "Canceled"


def check_validity():
    doctype = "Rental Quotation"
    re_docs = frappe.get_list(doctype, {
        "status": ["!=", "Expired"],
        "date": ["<", today()]
    })
    for row in re_docs:
        frappe.set_value(doctype, row.name, "status", "Expired")
    frappe.db.commit()


@frappe.whitelist()
def get_rental_estimation_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Rental Estimation", docname)
    response = {
        "name": doc.name,
        "customer":	doc.customer,
        "date":	doc.date,
        "valid_till":	doc.valid_till,
        "rate_type":	doc.rate_type,
        "re_items":	doc.items,
    }

    return response




def cust():
    res = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Address' and link_name = 'Hessa Alsarkal'""", as_dict=1)  
    return res[0]['parent']





