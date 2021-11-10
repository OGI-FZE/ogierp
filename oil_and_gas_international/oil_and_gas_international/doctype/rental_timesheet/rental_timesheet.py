# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class RentalTimesheet(Document):
	pass



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
