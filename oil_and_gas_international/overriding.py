import frappe,datetime
from frappe import _
from dateutil import relativedelta
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
			# self.create_job_card()





def disable_generating_serial_no(doc,handle=None):
	manufacturing_settings = frappe.get_doc("Manufacturing Settings")
	if doc.purpose == "Manufacturing":
		manufacturing_settings.set("make_serial_no_batch_from_work_order",1)
	elif doc.purpose in ["Inspection","Service"]:
		manufacturing_settings.set("make_serial_no_batch_from_work_order",0)
	manufacturing_settings.save()
	frappe.db.commit()



def accepted_serial_no_to_order(doc,handle=None):
	wo_jc = frappe.db.get_value("Job Card", {"name":doc.reference_name}, "work_order")
	wo = frappe.get_doc("Work Order", wo_jc)
	if wo.sales_order:
		order = frappe.get_doc("Sales Order", wo.sales_order)
	elif wo.rental_order:
		order = frappe.get_doc("Rental Order", wo.rental_order)

	if doc.status == "Accepted":
		for item in order.items:
			if item.item_code == doc.item_code:
				item.serial_no_accepted = "\n".join([item.serial_no_accepted,doc.item_serial_no])
				order.save()
				frappe.db.commit()


def add_transfered_qty_ro_item(doc,handle=None):
	if doc.rental_order:
		ro = frappe.get_doc("Rental Order", doc.rental_order)
		for item in doc.items:
			for i in ro.items:
				if item.item_code == i.item_code:
					if doc.return_from_rent:
						i.transfered_qty -= item.qty
					else:
						i.transfered_qty += item.qty
					ro.save()
					frappe.db.commit()





def create_rental_timesheet():
	ro_list = []
	ro = frappe.db.get_list('Rental Order',filters={'status': 'On Rent'},as_list=True)
	for i in range(len(ro)):
		ro_list.append(ro[i][0])
	for r in ro_list:
		ro_items = []
		rental_order = frappe.get_doc("Rental Order",r)
		timesheets = frappe.db.sql("""select name,start_date from `tabRental Timesheet`
										  where rental_order = '%s' order by start_date desc""" %(r),as_dict=1)
		if timesheets:
			last_ts = frappe.get_doc("Rental Timesheet",timesheets[0]['name'])
			new_ts = frappe.new_doc("Rental Timesheet")
			new_ts.customer = last_ts.customer
			new_ts.rental_order = last_ts.rental_order
			new_ts.start_date = last_ts.start_date + relativedelta.relativedelta(months=1, day=1)
			new_ts.end_date = last_ts.end_date + relativedelta.relativedelta(months=1, day=32)
			new_ts.currency = last_ts.currency
			new_ts.conversion_rate = last_ts.conversion_rate
			new_ts.price_list = last_ts.price_list

			for row in last_ts.items:
				new_ts.append("items",{
					"item_code": row.item_code,
					"item_name": row.item_name,
					"serial_no_accepted": row.serial_no_accepted,
					"description": row.description,
					"description_2": row.description_2,
					"customer_requirement": row.customer_requirement,
					"qty": row.qty,
					"rate": row.rate,
					"uom": row.uom,
					"operational_running": row.operational_running,
					"amount": row.amount,
					"standby": row.standby,
					"post_rental_inspection_charges": row.post_rental_inspection_charges,
					"lihdbr": row.lihdbr,
					"redress": row.redress,
					"straight": row.straight,
				})
			new_ts.save()
			frappe.db.commit()
			

def change_ro_status(doc,handle=None):
	if doc.end_date:
		doc.db_set("status","Completed")
	else:
		doc.db_set("status","On Rent")


