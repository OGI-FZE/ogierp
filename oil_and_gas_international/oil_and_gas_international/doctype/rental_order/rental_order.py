# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.controllers.accounts_controller import get_taxes_and_charges


class RentalOrder(Document):
    def on_submit(self):
        if self.rental_quotation:
            frappe.set_value("Rental Quotation",
                             self.rental_quotation, "status", "Ordered")
        self.db_set("status", "Submitted")
        frappe.db.commit()

    def on_update(self):
        pass

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