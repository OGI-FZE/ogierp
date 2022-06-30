# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.controllers.accounts_controller import get_taxes_and_charges


class RentalOrder(Document):
    def on_submit(self):
        if self.rental_quotation:
            self.status = "Open"
            frappe.set_value("Rental Quotation",
                             self.rental_quotation, "status", "Ordered")
        frappe.db.commit()

    def on_update(self):
        pass

    # def before_cancel(self):
    #     assets = frappe.get_list("Asset",filters={'rental_order':self.name})
    #     print("\n>>>>>>>>>>assets",assets)
    #     if assets:
    #         for asset in assets:
    #             print("\nasetttttttttttttttttttt",asset,asset.name)
    #             frappe.db.set_value("Asset", asset.name, "rental_order", '')


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