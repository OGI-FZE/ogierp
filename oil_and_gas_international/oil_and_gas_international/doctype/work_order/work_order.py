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
					for asset in assets:
						if asset:
							frappe.db.set_value("Asset", asset, "rental_status", "On hold for Inspection")

	def on_cancel(self):
		for row in self.items:
			assets = row.assets
			if assets:
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						frappe.db.set_value("Asset", asset, "rental_status", "Available for Rent")

	def on_trash(self):
		for row in self.items:
			assets = row.assets
			if assets:
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						frappe.db.set_value("Asset", asset, "rental_status", "Available for Rent")
