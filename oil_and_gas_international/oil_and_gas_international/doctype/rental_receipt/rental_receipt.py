# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today 

class RentalReceipt(Document):
	def validate(self):
		if (self.rental_stop_date and self.receipt_date) and (self.rental_stop_date > self.receipt_date):
			frappe.throw("Rental stop date can not be after rental receipt date")
		for row in self.items:
			assets = row.assets
			assets = assets.split("\n")
			serial_qty = 0
			for asset in assets:
				if asset:
					if not frappe.db.exists("Asset", asset):
						frappe.throw(f"Asset {asset} not exists!")

					status = frappe.get_value("Asset", asset, "rental_status")
					if status != "In Use":
						frappe.throw(
							f"Asset {asset} is not available for rent!")
					else:
						serial_qty = serial_qty + 1
			if serial_qty != row.qty:
				frappe.throw(
					f"Serial no's count({serial_qty}) not matched with the Qty({row.qty}) of the asset!")

	def on_cancel(self):
		self.set('status','Cancelled')
		for row in self.items:
			assets = row.assets
			assets = assets.split("\n")
			for asset in assets:
				if asset:
					frappe.db.set_value("Asset", asset, "rental_status", "In Use")
					if row.rental_order_item:
						cdt = "Rental Order Item"
						cdn = row.rental_order_item
						received_qty = frappe.get_value(cdt, cdn, "received_qty")
						frappe.set_value(cdt, cdn, "received_qty", int(received_qty) - int(row.qty))


	def on_submit(self):
		for row in self.items:
			assets = row.assets
			assets = assets.split("\n")
			for asset in assets:
				if asset:
					# updating asset status

					if self.rental_stop_date <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "In transit")
						
					if self.receipt_date <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "On hold for Inspection")
						frappe.db.set_value("Asset", asset, "rental_order", "")
					
					# updating rental order item status
					if row.rental_order_item:
						cdt = "Rental Order Item"
						cdn = row.rental_order_item
						qty = frappe.get_value(cdt, cdn, "qty")
						delivered_qty = frappe.get_value(cdt, cdn, "delivered_qty")
						received_qty = frappe.get_value(cdt, cdn, "received_qty")
						if not received_qty:
							received_qty = 0

						if received_qty > delivered_qty:
							frappe.throw(f"Can not receive more than remaining delivered qty in Rental Order Item({delivered_qty-received_qty})")
						
						frappe.set_value(cdt, cdn, "received_qty", int(received_qty) + int(row.qty))
						if received_qty == qty:
							frappe.set_value(cdt, cdn, "status", "Returned")

				  
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
					frappe.db.set_value("Asset", asset, "currently_with", "")
		self.set('status','Submitted')



@frappe.whitelist()
def get_rental_order_items(docname=None):
	if not docname:
		return {}

	doc = frappe.get_doc("Rental Order", docname)

	return doc.items
