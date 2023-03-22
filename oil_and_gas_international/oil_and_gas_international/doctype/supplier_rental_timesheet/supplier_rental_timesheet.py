# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today
from frappe.utils import date_diff


class SupplierRentalTimesheet(Document):
    def before_save(self):
        for row in self.items:
            row.delivery_date = self.start_date

    def validate(self):
        total = 0
        for row in self.items:
            if not row.amount:
                row.amount = 0 
            total += row.amount
        self.total_days = date_diff(self.end_date,self.start_date) + 1
        self.total_amount = total
        project = frappe.db.get_value("Project",{"rental_order":self.rental_order},"name")
        self.project = project
    def on_submit(self):
        self.update_subro_items_stopped_qty()
        self.generate_subrental_invoice()

    def update_subro_items_stopped_qty(self):
        subro = frappe.get_doc("Supplier Rental Order",self.supplier_rental_order)
        for row in self.items:
            if row.stop_rent:
                for item in subro.items:
                    if not item.stopped_qty:
                        item.stopped_qty = 0
                    if row.item_code == item.item_code:
                        item.stopped_qty += row.qty
        subro.save()
        frappe.db.commit()


    
    def generate_subrental_invoice(self):
        reninv = frappe.new_doc("Sub Rental Invoice")
        reninv.supplier = self.supplier
        reninv.company = self.company
        reninv.date = self.date
        reninv.sub_rental_order = self.supplier_rental_order
        reninv.division = self.division
        reninv.department = self.department
        reninv.currency = self.currency
        reninv.sub_rental_timesheet = self.name
        reninv.conversion_rate = self.conversion_rate
        reninv.total = self.total_amount
        reninv.from_date = self.start_date
        reninv.to_date = self.end_date
        reninv.total_qty = 0
        for row in self.items:
            reninv.total_qty += row.qty
            reninv.append("items",{
                "item_code": row.item_code,
                "item_name": row.item_name,
                "uom": row.uom,
                "qty": row.qty,
                "operational_running": row.operational_running,
                "rate": row.rate,
                "amount": row.amount,
                "standby": row.standby,
                "post_rental_inspection_charges": row.post_rental_inspection_charges,
                "lihdbr": row.lihdbr,
                "redress": row.redress,
                "straight": row.straight,
                "description":row.description,
                "days": row.days,
                "start_date_": row.start_date_,
                "end_date": row.end_date
            })
        reninv.save()
        frappe.db.commit()
    # def on_submit(self):
    # 	self.set('status','To Bill')

# @frappe.whitelist()
# def get_supplier_rental_order_items(docname=None):
# 	asset_list = []
    
# 	if not docname:
# 		return {}

    
# 	re_items = frappe.get_list("Supplier Rental Order Item", {
# 		"status": ["!=", "On Hold"],
# 		"parent": docname
# 	}, ["*"])
# 	rt=frappe.get_doc("Sub Rental Receipt", {"sub_rental_order": docname})
# 	for itm in re_items:
# 		asset_dict = {}
# 		rti_assets = frappe.get_list("Sub Rental Receipt Item", {
#             "parent": rt.name,
#             "item_code":itm.item_code,
#             "docstatus":1,
#         }, ["assets"])
# 		if rti_assets:
# 			l = (rti_assets[0]['assets']).splitlines()
# 			for ast in l:
# 				status = frappe.db.get_value("Asset",ast,"rental_status")
# 				if not asset_dict:
# 					asset_dict = {'assets':ast}
# 				else:
# 					d = asset_dict['assets']

# 					asset_dict['assets'] = d+'\n'+ast
# 			itm.update(asset_dict) 
# 	return re_items