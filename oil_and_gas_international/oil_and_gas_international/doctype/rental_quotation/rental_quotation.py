# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentalQuotation(Document):
    def validate(self):
        address = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Address' and link_name = '%s'"""% (self.customer), as_dict=1)  
        contact = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Contact' and link_name = '%s'"""% (self.customer), as_dict=1)  
        cus_add = frappe.get_doc('Address',address[0]['parent'])
        cus_con = frappe.get_doc('Contact', contact[0]['parent'])
        self.customer_address = address[0]['parent']
        self.customer_contact = contact[0]['parent']
        self.address = cus_add.address_line1 + "\n" + cus_add.city + "\n" + cus_add.country
        self.contact = cus_con.phone + "\n" + cus_con.email_id
        rate_by_qty = []
        for row in self.items:
            if not row.estimate_rate:
                row.estimate_rate = 0
            rate_by_qty.append(row.qty*row.estimate_rate)
            total_rate_qty = sum(rate_by_qty)
            self.total_by_month = total_rate_qty*30
            
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