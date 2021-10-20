# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalOrder(Document):
    def on_submit(self):
        self.status = "Open"
        frappe.set_value("Rental Quotation",
                         self.rental_quotation, "status", "Ordered")
        frappe.db.commit()


@frappe.whitelist()
def get_rental_quotation_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Rental Quotation", docname)
    response = {
        "name": doc.name,
        "customer":	doc.customer,
        "date":	doc.date,
        "rq_items":	doc.items,
    }

    return response
