# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalQuotation(Document):
    pass


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
