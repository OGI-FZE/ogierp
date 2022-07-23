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
			if row.assets:
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
								f"Asset {asset} is not in use!")
						else:
							serial_qty = serial_qty + 1
						#If tubular,
						# asset_doc = frappe.get_doc("Asset",asset)
						# if asset_doc.is_string_asset:
						# 	for ast in asset_doc.get("tubulars"):
						# 		if not frappe.db.exists("Asset", ast.asset):
						# 			frappe.throw(f"Tubular Asset {ast.asset} not exists!")

						# 		status = frappe.get_value("Asset", ast.asset, "rental_status")
						# 		if status != "In Use":
						# 			frappe.throw(
						# 				f"Tubular Asset {ast.asset} is not in use!")
				if serial_qty != row.qty:
					frappe.throw(
						f"Serial no's count({serial_qty}) not matched with the Qty({row.qty}) of the asset!")

	def on_cancel(self):
		self.set('status','Cancelled')
		for row in self.items:
			if not row.is_string:
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
						asset_doc = frappe.get_doc("Asset",asset)
						# if asset_doc.is_string_asset:
						# 	for ast in asset_doc.get("tubulars"):
						# 		frappe.db.set_value("Asset", ast.asset, "rental_status", "In Use")
						# 		frappe.db.set_value("Tubulars", ast.name, "rental_status", "In Use")
			else:
				item_doc = frappe.get_doc("Item",row.item_code)
				assets_in_use = item_doc.assets_in_use + row.qty
				assets_available_for_rent = item_doc.total_assets - assets_in_use
				frappe.db.set_value("Item",row.item_code,'assets_in_use',assets_in_use)
				frappe.db.set_value("Item",row.item_code,'assets_available_for_rent',assets_available_for_rent)




	def on_submit(self):
		for row in self.items:
			if not self.rental_stop_date:
				frappe.throw("Please provide rental stop date")
			if not self.receipt_date:
				frappe.throw("Please provide receipt date")
			if not row.is_string:
				assets = row.assets
				assets = assets.split("\n")
				for asset in assets:
					if asset:
						asset_doc = frappe.get_doc("Asset",asset)
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

							# if received_qty > delivered_qty:
							# 	frappe.throw(f"Can not receive more than remaining delivered qty in Rental Order Item({delivered_qty-received_qty})")
							
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
						#If tubular,
						# if asset_doc.is_string_asset:
						# 	for ast in asset_doc.get("tubulars"):
						# 		if self.rental_stop_date <= today():
						# 			frappe.db.set_value("Asset", ast.asset, "rental_status", "In transit")
						# 			frappe.db.set_value("Tubulars", ast.name, "rental_status", "In transit")
									
						# 		if self.receipt_date <= today():
						# 			frappe.db.set_value("Asset", ast.asset, "rental_status", "On hold for Inspection")
						# 			# frappe.db.set_value("Asset", ast.asset, "rental_order", "")
						# 			frappe.db.set_value("Tubulars", ast.name, "rental_status", "On hold for Inspection")
						# 		frappe.db.set_value("Tubulars", ast.name, "location", row.asset_location)
						# 		# asset movement
						# 		asset_location = frappe.get_value("Asset", ast.asset, "location")
						# 		if asset_location != row.asset_location:
						# 			asset_movement_doc = frappe.get_doc({
						# 				"doctype": "Asset Movement",
						# 				"transaction_date": today(),
						# 				"purpose": "Transfer"
						# 			})
						# 			asset_movement_doc.append("assets", {
						# 				"asset": ast.asset,
						# 				"target_location": row.asset_location
						# 			})
						# 			asset_movement_doc.save()
						# 			asset_movement_doc.submit()

						# 		frappe.db.commit()
						# 		frappe.db.set_value("Asset", ast.asset, "currently_with", "")

			else:
				item_doc = frappe.get_doc("Item",row.item_code)
				assets_in_use = item_doc.assets_in_use - row.qty
				assets_available_for_rent = item_doc.total_assets - assets_in_use
				frappe.db.set_value("Item",row.item_code,'assets_in_use',assets_in_use)
				frappe.db.set_value("Item",row.item_code,'assets_available_for_rent',assets_available_for_rent)						

		self.set('status','Submitted')



@frappe.whitelist()
def get_rental_order_items(docname=None):
	if not docname:
		return {}

	doc = frappe.get_doc("Rental Order", docname)

	return doc.items

@frappe.whitelist()
def get_rental_issue_assets(ro=None,item_code=None):
	asset_list =[]
	rin_list = frappe.db.get_list("Rental Issue Note",{'rental_order':ro,'docstatus':1},['name'])
	for rin in rin_list:
		rin = frappe.get_doc("Rental Issue Note",rin.name)
		for row in rin.items:
			if row.item_code == item_code:
				assets = row.assets
				assets = assets.split("\n")
				asset_list = list(set(asset_list + assets))

	return asset_list
