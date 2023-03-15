# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class ProjectWorkOrder(Document):
	def validate(self):
		items = [self.sales_order_items,self.rental_order_items]
		total = 0 
		if not self.for_returned_material:
			for item in items:
				if item:
					for i in item: 
						total += i.qty
						if item == self.sales_order_items:
							order_qty = frappe.db.sql("""select sum(qty) as qty
											from `tabSales Order Item`
											where parent = '%s'""" %(self.sales_order), as_dict=1)
						elif item == self.rental_order_items:
							order_qty = frappe.db.sql("""select sum(qty) as qty
												from `tabRental Order Item`
												where parent = '%s'""" %(self.rental_order),as_dict=1)
					if float(total) > float(order_qty[0].qty):
						frappe.throw(_("Quantity selected more than order quantity"))

				
