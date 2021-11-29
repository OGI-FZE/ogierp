# Copyright (c) 2021, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
class RentalOrderItemStatus(Document):
    
	def autoname(self):
		self.name = self.item_status.replace(" ","_").lower()
		print (self.name)
	
	def on_submit(self):
		execute(self)
	
	def on_cancel(self):
		delete(self)

def execute(self):
	create_custom_field("Rental Order Item", {
		"label": self.item_status,
		"fieldname": self.name,
		"fieldtype": "Currency",
		"options":'Currency',
		"insert_after": "total_amount",
	})
	frappe.db.commit()

def delete(self):
	del_name='Rental Order Item-'+self.name
	custom_field_doc = frappe.get_doc('Custom Field', del_name)
	custom_field_doc.delete()
