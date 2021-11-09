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
