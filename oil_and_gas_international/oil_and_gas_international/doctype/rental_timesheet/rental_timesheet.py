# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RentalTimesheet(Document):
	pass



@frappe.whitelist()
def get_rental_order_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Rental Order", docname)

    return doc.items
