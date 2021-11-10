import frappe
import json


@frappe.whitelist()
def get_timesheet(rental_orders=None):
    rental_orders = json.loads(rental_orders)
    if not rental_orders:
        return []

    timesheet_docs = frappe.get_list("Rental Timesheet", {
        "rental_order": ["in", rental_orders]
    }, ["name"])

    timesheet_docs = [row.name for row in timesheet_docs]

    timesheets = frappe.get_list("Rental Timesheet Item", {
                                 "parent": ["in", timesheet_docs],
                                 "is_billed": 0
                                 }, ["*"])

    return timesheets


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
