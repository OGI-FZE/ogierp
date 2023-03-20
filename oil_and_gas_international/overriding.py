import frappe,datetime
from frappe import _
from dateutil import relativedelta
from frappe.model.document import Document
from erpnext.controllers.accounts_controller import get_taxes_and_charges
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder
from datetime import datetime
from frappe.utils import date_diff



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
										  where rental_order = '%s' 
										  order by start_date desc""" %(r),as_dict=1)
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
			print(last_ts.name)
			for row in last_ts.items:
				if not row.stop_rent:
					new_ts.append("items",{
						"item_code": row.item_code,
						"item_name": row.item_name,
						# "serial_no_accepted": row.serial_no_accepted,
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
						"delivery_date": last_ts.start_date + relativedelta.relativedelta(months=1, day=1),
						"start_date_": last_ts.start_date + relativedelta.relativedelta(months=1, day=1),
						"end_date": last_ts.end_date + relativedelta.relativedelta(months=1, day=32)
					})
			new_ts.save()
			frappe.db.commit()
			

def change_ro_status(doc,handle=None):
	if doc.end_date:
		timesheets = frappe.db.sql("""select name,start_date from `tabRental Timesheet`
									where rental_order = '%s' order by start_date desc""" %(doc.name),as_dict=1)
		if timesheets:
			last_ts = frappe.get_doc("Rental Timesheet",timesheets[0]['name'])
			d = last_ts.end_date
			# if not isinstance(doc.end_date, datetime.date):
			# 	end_date = datetime.strptime(doc.end_date,"%Y-%M-%d")
			# else:
			# 	end_date = doc.end_date
			if datetime.strptime(doc.end_date,"%Y-%m-%d") < datetime(d.year,d.month,d.day):
				frappe.throw(_("End date is invalid, please set it after timesheet end date {}".format(d)))
		doc.db_set("status","Completed")
	else:
		doc.db_set("status","On Rent")


@frappe.whitelist()
def inspect_returned_serial_no(ro=None,item_code=None,stock_entry=None,serial_no=None):
	doc = frappe.new_doc("Inspection")
	doc.item_code = item_code
	doc.rental_order = ro
	doc.stock_entry = stock_entry
	doc.serial_no_to_inspect = serial_no
	doc.item_category = frappe.db.get_value("Item",item_code,"item_category")
	doc.return_from_rent = 1
	doc.save()
	frappe.db.commit()
	frappe.msgprint(_("inspection {} is created against this stock entry".format(doc.name)))


@frappe.whitelist()
def getTax(tx=None):
	# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Here>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
	taxes = get_taxes_and_charges('Sales Taxes and Charges Template',tx)
	return taxes


def set_item_rent_days(doc,handle=None):
	
	doc.total_amount = 0
	for row in doc.items:
		# if not row.start_date_ or row.end_date:
		# 	frappe.throw(_("please set start and end date for each item"))
		if doc.doctype in ['Sub Rental Invoice','Rental Invoice']:
			row.delivery_date = doc.from_date
		else:
			row.delivery_date = doc.start_date
	
		row.days = date_diff(row.end_date,row.start_date_) + 1
		row.amount = row.qty*row.rate*row.days
		doc.total_amount += row.amount
	


def get_income_expense_accounts(item=None,company=None):
	item = frappe.get_doc("Item",item)
	income_account = item.item_defaults[0].income_account
	expense_account = item.item_defaults[0].expense_account
	if expense_account == None:
		expense_account = frappe.db.get_value("Company",company,"default_expense_account")
	return income_account,expense_account

@frappe.whitelist()
def wo_qty_for_returned_item(rental_order=None,item_code=None):
	qty = frappe.db.sql("""select sum(qty) as qty
			from `tabWork Order`
			where rental_order='%s' and for_returned_material= 1
			and production_item ='%s' """ %(rental_order,item_code), as_dict=1)
	return qty[0].qty or 0


def check_rental_wo_qty(doc,handle=None):
	for item in doc.rental_order_items:
		wo_qty = wo_qty_for_returned_item(doc.rental_order,item.item_code)
		if doc.for_returned_material:
			if float(wo_qty) + (item.qty) > item.returned_qty:
				frappe.throw(_("you overpassed quantity"))
 



def get_pricing_rule(item_code=None):
    pr_list = []
    pricing_rules = frappe.db.sql("""select parent from `tabPricing Rule Item Code` where item_code = '%s'""" %(item_code))
    for pr in pricing_rules:
        pr_list.append(pr[0])
    return pr_list


@frappe.whitelist()
def get_rental_settings():
    settings = frappe.get_doc("Rental Division Settings")
    operationel = settings.operational_running
    lih_dbr = settings.lih_dbr
    straight = settings.straight
    standby = settings.standby
    redress = settings.redress
    post_rental_inspection_charges = settings.post_rental_inspection_charges
    return {"operationel":operationel,
            "lih_dbr":lih_dbr,
            "straight":straight,
            "standby":standby,
            "redress":redress,
            "post_rental_inspection_charges":post_rental_inspection_charges}


@frappe.whitelist()
def get_subrental_settings():
    settings = frappe.get_doc("Rental Division Settings")
    operationel = settings.rent_operational_running
    lih_dbr = settings.rent_lih_dbr
    straight = settings.rent_straight
    standby = settings.rent_standby
    redress = settings.rent_redress
    post_rental_inspection_charges = settings.rent_post_rental_inspection_charges
    return {"operationel":operationel,
            "lih_dbr":lih_dbr,
            "straight":straight,
            "standby":standby,
            "redress":redress,
            "post_rental_inspection_charges":post_rental_inspection_charges}



# def apply_pricing_rule(doc,handle=None):
#     for item in doc.items:
#         pr_list = get_pricing_rule(item.item_code)
#         for pr in pr_list:
#             buying = frappe.db.get_value("Price List",pr,"buying")
#             customer = frappe.db.get_value("Price List",pr,"customer")
#             if buying == 1 and customer == doc.customer:
#                 selected_pr = frappe.get_doc("Price List", pr)
#                 if selected_pr.valid_from < doc.date < selected_pr.valid_upto:
#                     if min_qty != 0 and max_qty !=0:
#                         if selected_pr.rate_or_discount == "Discount Percentage":
#                             if selected_pr.for_price_list == get_rental_settings()['operationel']:
#                                 item.base_operational_running = item.base_operationnel_running*discount_percentage/100
#                             if selected_pr.for_price_list == get_rental_settings()['lih_dbr']:
#                                 item.base_lihdbr = item.base_lihdbr*discount_percentage/100
#                             if selected_pr.for_price_list == get_rental_settings()['base_post_rental_inspection_charges']:
#                                 item.base_post_rental_inspection_charges = item.base_post_rental_inspection_charges*discount_percentage/100
#                             if selected_pr.for_price_list == get_rental_settings()['base_standby']:
#                                 item.base_standby = item.base_standby*discount_percentage/100
#                             if selected_pr.for_price_list == get_rental_settings()['base_straight']:
#                                 item.base_straight = item.base_straight*discount_percentage/100
#                             if selected_pr.for_price_list == get_rental_settings()['operationel']:
#                                 item.base_redress = item.base_redress*discount_percentage/100



def update_serial_no(doc,handle=None):
	if not doc.need_inspection and doc.stock_entry_type == "Material Receipt" and doc.sub_rental_order: 
		ro = frappe.get_doc("Rental Order",doc.rental_order)
		for roitem in ro.items:
			for item in doc.items:
				if roitem.item_code == item.item_code:
					roitem.serial_no_accepted = "\n".join([roitem.serial_no_accepted,item.serial_no])
					ro.save()
					frappe.db.commit()





def change_subro_status(doc,handle=None):
	if doc.end_date:
		timesheets = frappe.db.sql("""select name,start_date from `tabSupplier Rental Timesheet`
									where supplier_rental_order = '%s' order by start_date desc""" %(doc.name),as_dict=1)
		if timesheets:
			last_ts = frappe.get_doc("Rental Timesheet",timesheets[0]['name'])
			d = last_ts.end_date
			# if not isinstance(doc.end_date, datetime.date):
			# 	end_date = datetime.strptime(doc.end_date,"%Y-%M-%d")
			# else:
			# 	end_date = doc.end_date
			if datetime.strptime(doc.end_date,"%Y-%m-%d") < datetime(d.year,d.month,d.day):
				frappe.throw(_("End date is invalid, please set it after timesheet end date {}".format(d)))
		doc.db_set("status","Completed")
	else:
		doc.db_set("status","On Rent")


def create_sub_rental_timesheet():
	ro_list = []
	ro = frappe.db.get_list('Supplier Rental Order',filters={'status': 'On Rent'},as_list=True)
	for i in range(len(ro)):
		ro_list.append(ro[i][0])
	for r in ro_list:
		ro_items = []
		rental_order = frappe.get_doc("Supplier Rental Order",r)
		timesheets = frappe.db.sql("""select name,start_date from `tabSupplier Rental Timesheet`
										  where supplier_rental_order = '%s' 
										  order by start_date desc""" %(r),as_dict=1)
		if timesheets:
			last_ts = frappe.get_doc("Supplier Rental Timesheet",timesheets[0]['name'])
			new_ts = frappe.new_doc("Supplier Rental Timesheet")
			new_ts.supplier = last_ts.supplier
			new_ts.supplier_rental_order = last_ts.supplier_rental_order
			new_ts.start_date = last_ts.start_date + relativedelta.relativedelta(months=1, day=1)
			new_ts.end_date = last_ts.end_date + relativedelta.relativedelta(months=1, day=32)
			new_ts.currency = last_ts.currency
			new_ts.conversion_rate = last_ts.conversion_rate
			print(last_ts.name)
			for row in last_ts.items:
				if not row.stop_rent:
					new_ts.append("items",{
						"item_code": row.item_code,
						"item_name": row.item_name,
						"description": row.description,
						"qty": row.qty,
						"rate": row.rate,
						"uom": row.uom,
						"price_list": row.price_list,
						"operational_running": row.operational_running,
						"amount": row.amount,
						"standby": row.standby,
						"post_rental_inspection_charges": row.post_rental_inspection_charges,
						"lihdbr": row.lihdbr,
						"redress": row.redress,
						"straight": row.straight,
						"delivery_date": last_ts.start_date + relativedelta.relativedelta(months=1, day=1),
						"start_date_": last_ts.start_date + relativedelta.relativedelta(months=1, day=1),
						"end_date": last_ts.end_date + relativedelta.relativedelta(months=1, day=32)
					})
			new_ts.save()
			frappe.db.commit()