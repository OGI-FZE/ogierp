# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class RentalTimesheet(Document):
    def on_submit(self):
        self.set('status','To Bill')



@frappe.whitelist()
def get_rental_order_items(docname=None):
    asset_list = []
    
    if not docname:
        return {}
    
    re_items = frappe.get_list("Rental Order Item", {
        "status": ["!=", "On Hold"],
        "parent": docname
    }, ["*"])
    
    rt=frappe.get_doc("Rental Issue Note", {"rental_order": docname})
    for itm in re_items:
        asset_dict = {}
        rti_assets = frappe.get_list("Rental Issue Note Item", {
            "parent": rt.name,
            "item_code":itm.item_code,
            "docstatus":1,
        }, ["assets"])
        if rti_assets:
            # l = (rti_assets[0]['assets']).splitlines()
            # for ast in l:
            status = frappe.db.get_value("Asset",rti_assets[0]['assets'],"rental_status")
            if status == 'In Use':
                itm.update({'assets':rti_assets[0]['assets']})
            #     if not asset_dict:
            #         asset_dict = {'assets':rti_assets[0]['assets']}
            #     else:
            #         d = asset_dict['assets']

            #         asset_dict['assets'] = d+'\n'+rti_assets[0]['assets']
            # itm.update(asset_dict) 

    return re_items

@frappe.whitelist()
def check_issue_note(docname=None,itm=None):
    if not docname:
        return {}
    rt=frappe.get_doc("Rental Issue Note", {"rental_order": docname})

    rti = frappe.get_list("Rental Issue Note Item", {
        "parent": rt.name,
        "item_code":itm,
        "docstatus":1,
    }, ["item_code","item_name","assets"])
    return rti