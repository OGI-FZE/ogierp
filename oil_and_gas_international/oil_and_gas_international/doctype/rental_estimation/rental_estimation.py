# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentalEstimation(Document):
    pass


def check_validity(doc):
    if(doc.date < today):
        doc.status == "Expired"
        doc.save()
        doc.notify_update()


@frappe.whitelist()
def get_opportunity_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Opportunity", docname)
    return {
        "name": doc.name,
        "party_name": doc.party_name,
        "opportunity_items": doc.items
    }
