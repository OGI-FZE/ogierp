# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today
from frappe.utils import date_diff

class RentalTimesheet(Document):
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
        self.generate_rental_invoice()
        self.update_ro_items_stopped_qty()

    

    def update_ro_items_stopped_qty(self):
        ro = frappe.get_doc("Rental Order",self.rental_order)
        for row in self.items:
            if row.stop_rent:
                for item in ro.items:
                    if not item.stopped_qty:
                        item.stopped_qty = 0
                    if row.item_code == item.item_code:
                        item.stop_qty += row.qty
        ro.save()
        frappe.db.commit()
                
    def generate_rental_invoice(self):
        reninv = frappe.new_doc("Rental Invoice")
        reninv.customer = self.customer
        reninv.company = self.company
        reninv.date = self.date
        reninv.project = self.project
        reninv.rental_timesheet = self.name
        reninv.rental_order = self.rental_order
        reninv.division = self.division
        reninv.department = self.department
        reninv.currency = self.currency
        # reninv.selling_price_list = self.price_list
        reninv.conversion_rate = self.conversion_rate
        reninv.currency = self.currency
        reninv.price_list_currency = self.currency
        reninv.delivery_date = self.items[0].delivery_date
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
                "description_2": row.description_2,
                "customer_requirement": row.customer_requirement,
                "days": row.days,
                "start_date_": row.start_date_,
                "end_date": row.end_date
            })
        reninv.save()
        frappe.db.commit()
# @frappe.whitelist()
# def get_rental_order_items_old(docname=None):
#     if not docname:
#         return {}

#     doc = frappe.get_doc("Rental Order", docname)

#     return doc.items

# @frappe.whitelist()
# def get_rental_order_items(docname=None):
#     asset_list = []
    
#     if not docname:
#         return {}
    
#     re_items = frappe.get_list("Rental Order Item", {
#         "status": ["!=", "On Hold"],
#         "parent": docname
#     }, ["*"])
    
#     rt=frappe.get_doc("Rental Issue Note", {"rental_order": docname})
#     for itm in re_items:
#         asset_dict = {}
#         rti_assets = frappe.get_list("Rental Issue Note Item", {
#             "parent": rt.name,
#             "item_code":itm.item_code,
#             "docstatus":1,
#         }, ["assets"])
#         if rti_assets:
#             if rti_assets[0]['assets']:
#                 l = (rti_assets[0]['assets']).splitlines()
#                 for ast in l:
#                     status = frappe.db.get_value("Asset",ast,"rental_status")
#                     if status == 'In Use':
#                         if not asset_dict:
#                             asset_dict = {'assets':ast}
#                         else:
#                             d = asset_dict['assets']

#                             asset_dict['assets'] = d+'\n'+ast
#                 itm.update(asset_dict) 
            
#             # for ast in l:
#             #     status = frappe.db.get_value("Asset",rti_assets[0]['assets'],"rental_status")
#             #     if status == 'In Use':
#                     # itm.update({'assets':rti_assets[0]['assets']})
#                 #     if not asset_dict:
#                 #         asset_dict = {'assets':rti_assets[0]['assets']}
#                 #     else:
#                 #         d = asset_dict['assets']

#                 #         asset_dict['assets'] = d+'\n'+rti_assets[0]['assets']
#                 # itm.update(asset_dict) 
#     return re_items

# @frappe.whitelist()
# def check_issue_note(docname=None,itm=None):
#     if not docname:
#         return {}
#     rt=frappe.get_doc("Rental Issue Note", {"rental_order": docname})

#     rti = frappe.get_list("Rental Issue Note Item", {
#         "parent": rt.name,
#         "item_code":itm,
#         "docstatus":1,
#     }, ["item_code","item_name","assets","qty"])
#     return rti
