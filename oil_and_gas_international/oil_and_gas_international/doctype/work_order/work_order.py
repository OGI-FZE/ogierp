# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Work_Order(Document):

	def on_submit(self):
		for row in self.items:
			# assets = row.assets
			# assets = assets.split("\n")
			# for asset in assets:
			if row.assets:
				# rental_status = frappe.get_value(
				#     "Asset", asset, "rental_status")
				frappe.db.set_value("Asset", row.assets, "rental_status", "Available for Rent")

	def validate(self):
		if self.docstatus == 0:
			for row in self.items:
				# assets = row.assets
				# assets = assets.split("\n")
				# for asset in assets:
				if row.assets:
					frappe.db.set_value("Asset", row.assets, "rental_status", "On hold for Inspection")