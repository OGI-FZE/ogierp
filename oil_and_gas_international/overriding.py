import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder


class CustomWorkOrder(WorkOrder):

	def validate_sales_order(self):
		if self.sales_order:
			self.check_sales_order_on_hold_or_close()
			so = frappe.db.sql(
				"""
				select so.name, so_item.delivery_date, so.project
				from `tabSales Order` so
				inner join `tabSales Order Item` so_item on so_item.parent = so.name
				left join `tabProduct Bundle Item` pk_item on so_item.item_code = pk_item.parent
				where so.name=%s and so.docstatus = 1
					and so.skip_delivery_note  = 0 and (
					so_item.item_code=%s or
					pk_item.item_code=%s )
			""",
				(self.sales_order, self.production_item, self.production_item),
				as_dict=1,
			)

			if not so:
				so = frappe.db.sql(
					"""
					select
						so.name, so_item.delivery_date, so.project
					from
						`tabSales Order` so, `tabSales Order Item` so_item, `tabPacked Item` packed_item
					where so.name=%s
						and so.name=so_item.parent
						and so.name=packed_item.parent
						and so.skip_delivery_note = 0
						and so_item.item_code = packed_item.parent_item
						and so.docstatus = 1 and packed_item.item_code=%s
				""",
					(self.sales_order, self.production_item),
					as_dict=1,
				)

			if len(so):
				if not self.expected_delivery_date:
					self.expected_delivery_date = so[0].delivery_date

				if so[0].project:
					self.project = so[0].project

				if not self.material_request:
					self.validate_work_order_against_so()

	def on_submit(self):
		if not self.wip_warehouse and not self.skip_transfer:
			frappe.throw(_("Work-in-Progress Warehouse is required before Submit"))
		if not self.fg_warehouse:
			frappe.throw(_("For Warehouse is required before Submit"))

		if self.production_plan and frappe.db.exists(
			"Production Plan Item Reference", {"parent": self.production_plan}
		):
			self.update_work_order_qty_in_combined_so()
		else:
			self.update_work_order_qty_in_so()

		self.update_reserved_qty_for_production()
		self.update_completed_qty_in_material_request()
		self.update_planned_qty()
		self.update_ordered_qty()





def disable_generating_serial_no(doc,handle=None):
	manufacturing_settings = frappe.get_doc("Manufacturing Settings")
	if doc.purpose == "Manufacturing":
		manufacturing_settings.set("make_serial_no_batch_from_work_order",1)
	elif doc.purpose == "Inspection":
		manufacturing_settings.set("make_serial_no_batch_from_work_order",0)
	manufacturing_settings.save()
	frappe.db.commit()

# def set_serial_no_parent_group(doc,handle=None):
# 	pg = frappe.db.get_value("Item Group",{"name":doc.item_group},"parent_for_serial_no")
# 	doc.parent_grozdxhfdfghaup = pg


