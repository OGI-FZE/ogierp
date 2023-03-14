import frappe
import json
from frappe.utils import today


@frappe.whitelist()
def get_rental_timesheet_items(docname=None):
    if not docname:
        return {}
    
    re_items = frappe.get_list("Rental Timesheet Item", {
        "parent": docname
    }, ["*"])
    for row in re_items:
        itm = frappe.get_doc("Item",row.item_code)
        row.update({'item_name':itm.item_name})
        row.update({'item_group':itm.item_group})
    return re_items

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
def get_retal_order_rate(si_items,timesheet):
    items = json.loads(si_items)
    values=[]
    re_items = frappe.get_list("Rental Timesheet Item", {
        "parent": timesheet
    }, ["*"])
    for row in items:
        for itm in re_items:
            if row['asset_item'] and row['asset_item']==itm.item_code :
                values.append({'amount':itm.amount})

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

def get_desc(doc,method=None):
    pass

