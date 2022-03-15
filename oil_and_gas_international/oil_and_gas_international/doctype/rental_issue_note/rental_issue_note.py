# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class RentalIssueNote(Document):
	def validate(self):
		if self.date > self.rental_start_date:
			frappe.throw("Rental issue date can not be after rental start date")
		for row in self.items:
			# assets = row.assets
			# assets = assets.split("\n")
			serial_qty = 0
			# for asset in assets:
			if row.assets:
				if not frappe.db.exists("Asset", row.assets):
					frappe.throw(f"Asset {row.assets} not exists!")

				status = frappe.get_value("Asset", row.assets, "rental_status")
				if status != "Available for Rent":
					frappe.throw(
						f"Asset {row.assets} is not available for rent!")
				else:
					serial_qty = serial_qty + 1
			if serial_qty != row.qty:
				frappe.throw(
					f"Serial no's count({serial_qty}) not matched with the Qty({row.qty}) of the asset!")

	def on_cancel(self):
		self.set('status','Cancelled')
		for row in self.items:
			# assets = row.assets
			# assets = assets.split("\n")
			# for asset in assets:
			if row.assets:
				frappe.db.set_value("Asset", row.assets, "rental_status", "Available for Rent")
				if row.rental_order_item:
					cdt = "Rental Order Item"
					cdn = row.rental_order_item
					delivered_qty = frappe.get_value(cdt, cdn, "delivered_qty")
					frappe.set_value(cdt, cdn, "delivered_qty", int(delivered_qty) - int(row.qty))


		movements = frappe.get_list("Asset Movement",filters={'rental_issue_note':self.name})
		for mov in movements:
			mov_doc = frappe.get_doc("Asset Movement",mov.name)
			if mov_doc.docstatus ==1:
				mov_doc.cancel()

	def before_submit(self):
		issue_notes = frappe.get_list("Work_Order",filters={'rental_issue_note':self.name,'docstatus':1})
		if not issue_notes:
			frappe.throw("Please create work order before submitting issue note")

	def on_submit(self):
		self.set('status','Submitted')
		for row in self.items:
			# assets = row.assets
			# assets = assets.split("\n")
			# for asset in assets:
			if row.assets:
				# updating asset status
				# issue date
				if self.date == today():
					frappe.db.set_value("Asset", row.assets, "rental_status", "In transit")
					
				if self.rental_start_date == today():# issue date
					frappe.db.set_value("Asset", row.assets, "rental_status", "In Use")
					frappe.db.set_value("Asset", row.assets, "rental_order", self.rental_order)
				
				# updating rental order item status
				if row.rental_order_item:
					cdt = "Rental Order Item"
					cdn = row.rental_order_item
					qty = frappe.get_value(cdt, cdn, "qty")
					delivered_qty = frappe.get_value(cdt, cdn, "delivered_qty")
					if not delivered_qty:
						delivered_qty = 0

					if (delivered_qty + 1) > qty:
						frappe.throw(f"Can not deliver asset(s) more than remaining qty in Rental Order Item({qty-delivered_qty})")
					
					frappe.set_value(cdt, cdn, "delivered_qty", int(delivered_qty) + int(row.qty))
					if (delivered_qty) == qty:
						frappe.set_value(cdt, cdn, "status", "Delivered")

			  
				# asset movement
				asset_location = frappe.get_value("Asset", row.assets, "location")
				if asset_location != row.asset_location:
					asset_movement_doc = frappe.get_doc({
						"doctype": "Asset Movement",
						"transaction_date": today(),
						"purpose": "Transfer",
						"rental_issue_note": self.name
					})
					asset_movement_doc.append("assets", {
						"asset": row.assets,
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

@frappe.whitelist()
def get_project(docname=None):
	if not docname:
		return 0

	proj = frappe.get_list("Project",fields = ["name"],filters = {'rental_order':docname})
	if proj:
		return proj[0]
	else:
		return 0