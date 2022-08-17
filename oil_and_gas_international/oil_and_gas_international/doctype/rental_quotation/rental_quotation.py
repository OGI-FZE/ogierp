# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentalQuotation(Document):
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
