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
    return doc
