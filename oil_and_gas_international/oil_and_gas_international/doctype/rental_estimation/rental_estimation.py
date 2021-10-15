# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalEstimation(Document):
    pass


@frappe.whitelist()
def get_opportunity_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Opportunity", docname)
    return doc
