import frappe
# from oil_and_gas_international.events.rental_estimation import check_validity as check_re_validity
# from oil_and_gas_international.events.rental_quotation import check_validity as check_rq_validity
from frappe.utils import today
from collections import Counter


def daily():
    # check_re_validity()
    # check_rq_validity()
    make_rental_timesheet()


def make_rental_timesheet():
    rental_order_items = frappe.get_list("Rental Order Item", {
        "status": ["!=", "On Hold"],
        "from_date": ["<=", today()],
        "to_date": [">=", today()]
    }, ["parent"])

    rental_orders = []
    for row in rental_order_items:
        rental_orders.append(row.parent)

    rental_orders = Counter(rental_orders)
    for row in rental_orders:
        rental_order = frappe.get_doc("Rental Order", row)
        ro_exists = frappe.db.exists({
            "doctype": "Rental Timesheet",
            "date": today(),
            "docstatus": 1
        })

        if not ro_exists:
            rental_timesheet = frappe.get_doc({
                "doctype": "Rental Timesheet",
                "customer": rental_order.customer,
                "rental_order": rental_order.name,
                "company": rental_order.company,
            })

            has_items = False
            for item in rental_order.items:
                if item.status != "on hold":
                    rental_assets = frappe.get_list(
                        "Rental Issue Note Item", {"rental_order_item": item.name}, ["assets"])
                    qty = 0
                    for row in rental_assets:
                        assets = row.assets
                        assets = assets.split("\n")
                        for asset in assets:
                            print(asset)
                            if asset:
                                rental_status = frappe.get_value(
                                    "Asset", asset, "rental_status")
                                if rental_status == "In Use":
                                    qty = qty + 1

                    if qty:
                        rental_timesheet.append("items", {
                            "item_code": item.item_code,
                            "qty": qty,
                            "rate": item.rate,
                            "asset_location": item.asset_location,
                        })
                        has_items = True

            if has_items:
                rental_timesheet.save()
                rental_timesheet.submit()

    frappe.db.commit()
