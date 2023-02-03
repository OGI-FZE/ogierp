# Copyright (c) 2023, Havenir Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document, _
import frappe


class Inspection(Document):
	def validate(self):

		warehouse_qty = frappe.db.get_value("Bin",{"item_code":self.item_code,"warehouse":self.warehouse},"actual_qty")
		if not warehouse_qty:
			warehouse_qty = 0
		parameters = [self.drill_collar_parameters,
					  self.heavy_weight_drill_pipe_parameters,
					  self.drill_pipe_parameters,
					  self.tubing_parameters,
					  self.near_stabilizer_parameters,
					  self.string_stabilizer_parameters,
					  self.drilling_tools_parameters]
		for parameter in parameters:
			if parameter:
				if float(warehouse_qty) < len(parameter):
					frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))

		# for row in self.drill_collar_parameters:
		# 	if not 3.42 < row.length <4:
		# 		row.status = "Failed"
		# 	else: row.status = "Validated"
		# 	if not row.condition:
		# 		row.status = "Failed"
	


@frappe.whitelist()
def create_wo(qty,item_code,warehouse=None,item_category=None,project=None,project_wo=None,sales_o=None,rental_o=None):
    new_doc = frappe.new_doc('Work Order')
    inspection_bom = frappe.db.get_value("BOM",{"item": item_code,"inspection_bom": 1}, "name")

    if float(qty) == 0:
        frappe.throw(_("You don't have Item : {} in warehouse {}")
                    .format(item_code,warehouse))
    if rental_o:
        qty_wo = frappe.db.sql("""select qty
								  from `tabWork Order` 
								  where rental_order = "%s" 
								  and production_item = "%s" 
								  and status != "Cancelled" """ %(rental_o,item_code),as_dict=1)
        qty_list = []
        for i in range(len(qty_wo)):   
            qty_list.append(qty_wo[i]['qty'])
        total_wo_qty = sum(qty_list)
        if float(total_wo_qty) + float(qty) > get_rental_order_item_qty(rental_o,item_code):
            frappe.throw(_("Cannot inspect more Item {} than Rental Order quantity {}".format(item_code,get_rental_order_item_qty(rental_o,item_code))))

    if not inspection_bom:
        frappe.throw(_("Item {} does not have an Inspection BOM, please create one and try again".format(item_code)))
    new_doc.division = "Inspection"
    new_doc.skip_transfer = 1
    new_doc.date = frappe.utils.nowdate()
    new_doc.fg_warehouse = warehouse
    new_doc.production_item = item_code
    new_doc.item_category = item_category
    new_doc.qty = float(qty)
    new_doc.sales_order = sales_o
    new_doc.rental_order = rental_o
    new_doc.project = project
    new_doc.project_wo = project_wo
    new_doc.bom_no = inspection_bom
    new_doc.save()
    frappe.db.commit()
    return "dddddd"



def get_rental_order_item_qty(rental_o="OGI-RO-01-2023-0030",item_code="17796"):
    item_qty = frappe.db.sql("""select qty
                                from `tabRental Order Item` 
                                where item_code = "%s" and parent = "%s" """ %(item_code,rental_o), as_dict=1)
    return item_qty[0]['qty']




