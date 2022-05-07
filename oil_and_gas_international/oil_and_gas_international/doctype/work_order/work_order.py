# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Work_Order(Document):

	def on_submit(self):
		for row in self.items:
			assets = row.assets
			if assets:
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						# rental_status = frappe.get_value(
						#     "Asset", asset, "rental_status")
						frappe.db.set_value("Asset", asset, "rental_status", "Available for Rent")

	def validate(self):
		if self.docstatus == 0:
			for row in self.items:
				assets = row.assets
				if assets:
					assets = assets.split("\n")
					serial_qty = 0
					for asset in assets:
						if asset:
							if not frappe.db.exists("Asset", asset):
								frappe.throw(f"Asset {asset} not exists!")

							status = frappe.get_value("Asset", asset, "rental_status")
							if self.rental_order:
								if status != "Available for Rent":
									frappe.throw(
										f"Asset {asset} is not available for rent!")
								else:
									serial_qty = serial_qty + 1
								if asset:
									frappe.db.set_value("Asset", asset, "rental_status", "On hold for Inspection")
							if self.sub_rental_order:
								if status != "On hold for Inspection":
									frappe.throw(
										f"Asset {asset} is not on hold for inspection!")
								else:
									serial_qty = serial_qty + 1
					if serial_qty != row.quantity:
						frappe.throw(
							f"Serial no's count({serial_qty}) not matched with the Qty({row.quantity}) of the asset!")

	def on_cancel(self):
		for row in self.items:
			assets = row.assets
			if assets:
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						if self.rental_order:
							frappe.db.set_value("Asset", asset, "rental_status", "Available for Rent")
						if self.sub_rental_order:
							frappe.db.set_value("Asset", asset, "rental_status", "On hold for Inspection")

	def on_trash(self):
		for row in self.items:
			assets = row.assets
			if assets:
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						if self.rental_order:
							frappe.db.set_value("Asset", asset, "rental_status", "Available for Rent")
						if self.sub_rental_order:
							frappe.db.set_value("Asset", asset, "rental_status", "On hold for Inspection")
