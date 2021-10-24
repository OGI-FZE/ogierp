# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentalIssueNote(Document):
    def validate(self):
        for row in self.items:
            assets = row.assets
            assets = assets.split("\n")
            serial_qty = 0
            for asset in assets:
                if asset:
                    if not frappe.db.exists("Asset", asset):
                        frappe.throw(f"Asset {asset} not exists!")

                    status = frappe.get_value("Asset", asset, "rental_status")
                    if status != "Available for Rent":
                        frappe.throw(
                            f"Asset {asset} is not available for rent!")
                    else:
                        serial_qty = serial_qty + 1
            if serial_qty != row.qty:
                frappe.throw(
                    f"Serial no's count({serial_qty}) not matched with the Qty({row.qty}) of the asset!")

    def on_submit(self):
        for row in self.items:
            assets = row.assets
            assets = assets.split("\n")
            for asset in assets:
                if asset:
                    # updating asset status
                    frappe.db.set_value("Asset", asset, "rental_status", "In Use")
                    
                    # updating rental order item status
                    if row.rental_order_item:
                        cdt = "Rental Order Item"
                        cdn = row.rental_order_item
                        qty = frappe.get_value(cdt, cdn, "qty")
                        delivered_qty = frappe.get_value(cdt, cdn, "delivered_qty")
                        if not delivered_qty:
                            delivered_qty = 0

                        if (delivered_qty + row.qty) > qty:
                            frappe.throw(f"Can not deliver asset(s) more than remaining qty in Rental Order Item({qty-delivered_qty})")
                        
                        frappe.set_value(cdt, cdn, "delivered_qty", int(delivered_qty) + int(row.qty))
                        if (delivered_qty + row.qty) == qty:
                            frappe.set_value(cdt, cdn, "status", "Delivered")

                  
                    # asset movement
                    asset_location = frappe.get_value("Asset", asset, "location")
                    if asset_location != row.asset_location:
                        asset_movement_doc = frappe.get_doc({
                            "doctype": "Asset Movement",
                            "transaction_date": today(),
                            "purpose": "Transfer"
                        })
                        asset_movement_doc.append("assets", {
                            "asset": asset,
                            "target_location": row.asset_location
                        })
                        asset_movement_doc.save()
                        asset_movement_doc.submit()

                    frappe.db.commit()


@frappe.whitelist()
def get_rental_order_items(docname=None):
    if not docname:
        return {}

    doc = frappe.get_doc("Rental Order", docname)

    return doc.items
