import frappe


@frappe.whitelist()
def get_rental_order_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Rental Order", docname)
    res = {
        "name": doc.name,
        "ro_items": doc.items,
    }
    return res