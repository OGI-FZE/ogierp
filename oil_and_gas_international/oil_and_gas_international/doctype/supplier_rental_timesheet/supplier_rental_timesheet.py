# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class SupplierRentalTimesheet(Document):
	def on_submit(self):
		self.set('status','To Bill')

@frappe.whitelist()
def get_supplier_rental_order_items(docname=None):
	asset_list = []
	
	if not docname:
		return {}

	
	re_items = frappe.get_list("Supplier Rental Order Item", {
		"status": ["!=", "On Hold"],
		"parent": docname
	}, ["*"])
	rt=frappe.get_doc("Sub Rental Receipt", {"sub_rental_order": docname})
	for itm in re_items:
		asset_dict = {}
		rti_assets = frappe.get_list("Sub Rental Receipt Item", {
            "parent": rt.name,
            "item_code":itm.item_code,
            "docstatus":1,
        }, ["assets"])
		if rti_assets:
			l = (rti_assets[0]['assets']).splitlines()
			for ast in l:
				status = frappe.db.get_value("Asset",ast,"rental_status")
				if not asset_dict:
					asset_dict = {'assets':ast}
				else:
					d = asset_dict['assets']

					asset_dict['assets'] = d+'\n'+ast
			itm.update(asset_dict) 
	return re_items