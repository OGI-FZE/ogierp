# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class RentalTimesheet(Document):
    def on_submit(self):
        self.set('status','To Bill')



@frappe.whitelist()
def get_rental_order_items(docname=None):
    if not docname:
        return {}
    
    re_items = frappe.get_list("Rental Order Item", {
        "status": ["!=", "On Hold"],
        "from_date": ["<=", today()],
        "to_date": [">=", today()],
        "parent": docname
    }, ["*"])

    return re_items

@frappe.whitelist()
def check_issue_note(docname=None,itm=None):
    if not docname:
        return {}
    rt=frappe.get_doc("Rental Issue Note", {"rental_order": docname})

    rti = frappe.get_list("Rental Issue Note Item", {
        "parent": rt.name,
        "item_code":itm,
        "docstatus":1
    }, ["*"])
    return len(rti)