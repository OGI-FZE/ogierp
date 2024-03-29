# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today


class RentalIssueNote(Document):
	def validate(self):
		if self.date > self.rental_start_date:
			frappe.throw("Rental issue date can not be after rental start date")
		for row in self.items:
			if row.assets:
				assets = row.assets
				assets = assets.split("\n")
				serial_qty = 0
				for asset in assets:
					if asset:
						asset_doc = frappe.get_doc("Asset",asset)
						if not frappe.db.exists("Asset", asset):
							frappe.throw(f"Asset {asset} not exists!")

						status = frappe.get_value("Asset", asset, "rental_status")
						if status != "Available for Rent":
							frappe.throw(
								f"Asset {asset} is not available for rent!")
						else:
							serial_qty = serial_qty + 1
						#If tubular,
						# if asset_doc.is_string_asset:
						# 	for ast in asset_doc.get("tubulars"):
						# 		if not frappe.db.exists("Asset", ast.asset):
						# 			frappe.throw(f"Tubular Asset {ast.asset} not exists!")

						# 		status = frappe.get_value("Asset", ast.asset, "rental_status")
						# 		if status != "Available for Rent":
						# 			frappe.throw(
						# 				f"Tubular Asset {ast.asset} is not available for rent!")

				if serial_qty != row.qty:
					frappe.throw(
						f"Serial no's count({serial_qty}) not matched with the Qty({row.qty}) of the asset!")

	def on_cancel(self):
		self.db_set("status", "Cancelled")
		for row in self.items:
			if not row.is_string:
				assets = row.assets
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						frappe.db.set_value("Asset", asset, "rental_status", "Available for Rent")
						if row.rental_order_item:
							cdt = "Rental Order Item"
							cdn = row.rental_order_item
							delivered_qty = frappe.get_value(cdt, cdn, "delivered_qty")
							frappe.set_value(cdt, cdn, "delivered_qty", int(delivered_qty) - 1)
						frappe.db.set_value("Asset", asset, "currently_with", '')
						frappe.db.set_value("Asset", asset, "issue_date", '')
						# asset_doc = frappe.get_doc("Asset",asset)
						# if asset_doc.is_string_asset:
						# 	for ast in asset_doc.get("tubulars"):
						# 		frappe.db.set_value("Asset", ast.asset, "rental_status", "Available for Rent")
						# 		frappe.db.set_value("Tubulars", ast.name, "rental_status", "Available for Rent")
			else:
				item_doc = frappe.get_doc("Item",row.item_code)
				assets_in_use = item_doc.assets_in_use - row.qty
				assets_available_for_rent = item_doc.total_assets - assets_in_use
				usage_status = item_doc.usage_status
				if item_doc.usage_status:
					upd = 0
					for line in item_doc.usage_status:
						if line.customer == self.customer:
							cdt = "Usage Status"
							cdn = line.name
							upd_qty = int(line.qty-row.qty)
							frappe.set_value(cdt, cdn, "qty", upd_qty)
							upd = 1
					
				frappe.db.set_value("Item",row.item_code,'assets_in_use',assets_in_use)
				frappe.db.set_value("Item",row.item_code,'assets_available_for_rent',assets_available_for_rent)						


		movements = frappe.get_list("Asset Movement",filters={'rental_issue_note':self.name})
		for mov in movements:
			mov_doc = frappe.get_doc("Asset Movement",mov.name)
			if mov_doc.docstatus ==1:
				mov_doc.cancel()

	def before_submit(self):
		issue_notes = frappe.get_list("Work_Order",filters={'rental_issue_note':self.name,'docstatus':1})
		if not issue_notes:
			frappe.throw("Please create work order before submitting issue note")
		for row in self.items:
			if row.is_string:
				item_doc = frappe.get_doc("Item",row.item_code)
				if row.qty > item_doc.assets_available_for_rent:
					frappe.throw(_("You can not issue more than available.\nAvailable Quantity:{0}").format(item_doc.assets_available_for_rent))


	def on_submit(self):
		self.db_set("status", "Submitted")
		for row in self.items:
			if not row.is_string:
				assets = row.assets
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						asset_doc = frappe.get_doc("Asset",asset)
						# updating asset status
						# issue date
						if (self.date == today()) or (self.date < today()):
							frappe.db.set_value("Asset", asset, "rental_status", "In transit")
							# frappe.db.set_value("Asset", asset, "rental_order", self.rental_order)
							
						if (self.rental_start_date == today()) or (self.rental_start_date < today()):# issue date
							frappe.db.set_value("Asset", asset, "rental_status", "In Use")
							# frappe.db.set_value("Asset", asset, "rental_order", self.rental_order)

						# updating rental order item status
						if row.rental_order_item:
							cdt = "Rental Order Item"
							cdn = row.rental_order_item
							qty = frappe.get_value(cdt, cdn, "qty")
							delivered_qty = frappe.get_value(cdt, cdn, "delivered_qty")
							if not delivered_qty:
								delivered_qty = 0

							# if (delivered_qty + 1) > qty:
							# 	frappe.throw(f"Can not deliver asset(s) more than remaining qty in Rental Order Item({qty-delivered_qty})")
							
							frappe.set_value(cdt, cdn, "delivered_qty", int(delivered_qty) + 1)
							if (delivered_qty) == qty:
								frappe.set_value(cdt, cdn, "status", "Delivered")

					  
						# asset movement
						asset_location = frappe.get_value("Asset", asset, "location")
						if asset_location != row.asset_location:
							asset_movement_doc = frappe.get_doc({
								"doctype": "Asset Movement",
								"transaction_date": today(),
								"purpose": "Transfer",
								"rental_issue_note": self.name
							})
							asset_movement_doc.append("assets", {
								"asset": asset,
								"target_location": row.asset_location
							})
							asset_movement_doc.save()
							asset_movement_doc.submit()

						frappe.db.commit()
						
						frappe.db.set_value("Asset", asset, "currently_with", self.customer)
						frappe.db.set_value("Asset", asset, "issue_date", today())
						#If tubular,
						# if asset_doc.is_string_asset:
						# 	for ast in asset_doc.get("tubulars"):
						# 		if (self.date == today()) or (self.date < today()):
						# 			frappe.db.set_value("Asset", ast.asset, "rental_status", "In transit")
						# 			frappe.db.set_value("Tubulars", ast.name, "rental_status", "In transit")
									
						# 		if (self.rental_start_date == today()) or (self.rental_start_date < today()):# issue date
						# 			frappe.db.set_value("Asset", ast.asset, "rental_status", "In Use")
						# 			frappe.db.set_value("Tubulars", ast.name, "rental_status", "In Use")

						# 		# asset movement

						# 		asset_location = frappe.get_value("Asset", ast.asset, "location")
						# 		if asset_location != row.asset_location:
						# 			asset_movement_doc = frappe.get_doc({
						# 				"doctype": "Asset Movement",
						# 				"transaction_date": today(),
						# 				"purpose": "Transfer",
						# 				"rental_issue_note": self.name
						# 			})
						# 			asset_movement_doc.append("assets", {
						# 				"asset": ast.asset,
						# 				"target_location": row.asset_location
						# 			})
						# 			asset_movement_doc.save()
						# 			asset_movement_doc.submit()

						# 		frappe.db.commit()
						# 		frappe.db.set_value("Tubulars", ast.name, "location", row.asset_location)
						# 		frappe.db.set_value("Asset", ast.asset, "currently_with", self.customer)
			else:
				item_doc = frappe.get_doc("Item",row.item_code)
				assets_in_use = item_doc.assets_in_use + row.qty
				assets_available_for_rent = item_doc.total_assets - assets_in_use
				usage_status = item_doc.usage_status
				if item_doc.usage_status:
					upd = 0
					for line in item_doc.usage_status:
						if line.customer == self.customer:
							cdt = "Usage Status"
							cdn = line.name
							frappe.set_value(cdt, cdn, "qty", int(line.qty+row.qty))
							upd = 1
					if not upd:
						item_doc.append('usage_status',{
								"customer":self.customer,
								"qty":row.qty
							})
						item_doc.save(ignore_permissions=True)
				else:
					item_doc.append('usage_status',{
							"customer":self.customer,
							"qty":row.qty
						})
					item_doc.save(ignore_permissions=True)

				frappe.db.set_value("Item",row.item_code,'assets_in_use',assets_in_use)
				frappe.db.set_value("Item",row.item_code,'assets_available_for_rent',assets_available_for_rent)


@frappe.whitelist()
def get_rental_order_items(docname=None):
	if not docname:
		return {}

	doc = frappe.get_doc("Rental Order", docname)
	# for i in doc.items:
	# 	cat = frappe.db.get_value("Asset", {"item_code": i.item_code}, "asset_category")

	# return [doc.items,cat]
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