# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SupplierRentalOrder(Document):
    def validate(self):
        if self.supplier:
            address = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Address' and link_name = '%s'"""% (self.supplier), as_dict=1)  
            contact = frappe.db.sql("""select parent from `tabDynamic Link` where parenttype = 'Contact' and link_name = '%s'"""% (self.supplier), as_dict=1)  
            if address:
                sup_add = frappe.get_doc('Address',address[0]['parent'])
                self.supplier_address = address[0]['parent']
                self.address_display = sup_add.address_line1 + "\n" + sup_add.city + "\n" + sup_add.country
            if contact:
                sup_con = frappe.get_doc('Contact', contact[0]['parent'])
                self.supplier_contact = contact[0]['parent']
                self.contact_display = sup_con.phone + "\n" + sup_con.email_id
    def on_submit(self):
        if self.start_date and not self.end_date:
            self.db_set("status","On Rent")
 

        # if self.supplier_rental_quotation:
        #     self.status = "Open"
        #     frappe.set_value("Supplier Rental Quotation", self.supplier_rental_quotation, "status", "Ordered")
        # frappe.db.commit()

    @frappe.whitelist()
    def get_supplier_rental_quotation_items(docname=None):
        if not docname:
            return {}

        doc = frappe.get_doc("Supplier Rental Quotation", docname)
        response = {
            "name": doc.name,
            "supplier":	doc.supplier,
            "date":	doc.date,
            "rate_type": doc.rate_type,
            "rq_items":	doc.items,
        }

        return response
