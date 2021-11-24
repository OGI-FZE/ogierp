import frappe
import json


@frappe.whitelist()
def get_rental_order_items(rental_orders=None):
    rental_orders = json.loads(rental_orders)
    if not rental_orders:
        return []

    items = frappe.get_list("Rental Order Item", {
                                 "parent": ["in", rental_orders],
                                 }, ["*"])

    return items


def validate(doc, method=None):
    for row in doc.items:
        if row.rental_timesheet_item:
            row.rate = frappe.db.get_value(
                "Rental Timesheet Item", row.rental_timesheet_item, "rate")


def on_submit(doc, method=None):
    for row in doc.items:
        if row.rental_timesheet_item:
            row.rate = frappe.db.set_value(
                "Rental Timesheet Item", row.rental_timesheet_item, "is_billed", 1)
