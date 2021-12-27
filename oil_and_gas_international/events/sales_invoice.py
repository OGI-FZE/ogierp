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

@frappe.whitelist()
def get_retal_order_rate(si_items):
    items = json.loads(si_items)
    values=[]
    for row in items:
        if 'rental_order_item' not in row:
            frappe.throw('Sales invoice is not linked with any rental order')
        total,billed = frappe.db.get_value(
            "Rental Order Item", row['rental_order_item'], ['total_amount','billed_amount'])
        values.append({
            'total':total,
            'billed':billed,
            })
    return values

def addbilledamount(doc, method=None):
    for row in doc.items:
        if row.rental_order_item:
            new_doc = frappe.get_doc("Rental Order Item", row.rental_order_item)
            new_doc.db_set('billed_amount',new_doc.billed_amount+row.rate )

    # for row in doc.items:
    #     if row.rental_timesheet_item:
    #         row.rate = frappe.db.get_value(
    #             "Rental Timesheet Item", row.rental_timesheet_item, "rate")

def removebilledamount(doc,method=None):
    for row in doc.items:
        if row.rental_order_item:
            new_doc = frappe.get_doc("Rental Order Item", row.rental_order_item)
            new_doc.db_set('billed_amount',new_doc.billed_amount-row.rate )
            
def on_submit(doc, method=None):
    for row in doc.items:
        if row.rental_timesheet_item:
            row.rate = frappe.db.set_value(
                "Rental Timesheet Item", row.rental_timesheet_item, "is_billed", 1)
