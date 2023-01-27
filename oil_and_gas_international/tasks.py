import frappe
# from oil_and_gas_international.events.rental_estimation import check_validity as check_re_validity
# from oil_and_gas_international.events.rental_quotation import check_validity as check_rq_validity
from frappe.utils import cstr, getdate, split_emails, add_days, today, get_last_day, get_first_day, month_diff
from collections import Counter
from frappe.utils import today




def aft_project(doc, handler=None):
	if doc.name != doc.project_name:
		doc.project_name = doc.name


def daily():
	# check_re_validity()
	# check_rq_validity()
	# make_rental_timesheet()

	# rental_estimation_validation()
	# rental_quotation_validation()
	# calc_rental_order_item_amount()
	change_rental_status()
	

def calc_rental_order_item_amount():
	rental_orders = frappe.get_list("Rental Order", {
		"status": "Open"
	}, ["name"])

	for ro in rental_orders:
		rental_order = frappe.get_doc("Rental Order", ro.name)
		for item in rental_order.items:
			if item.rental_status:
				price_list = frappe.get_value("Rental Order Item Status",
											  item.rental_status, "price_list")

				status_price = frappe.get_value("Item Price", {
					"item_code": item.item_code,
					"price_list": price_list
				}, "price_list_rate")
			   
				if not status_price:
					status_price = 0
				slug=item.rental_status
				slug=slug.replace(" ","_").lower()
				# item[slug] = item[slug] + status_price

				item.total_amount = item.total_amount + status_price

		rental_order.save()

	frappe.db.commit()


def make_rental_timesheet():
	rental_order_items = frappe.get_list("Rental Order Item", {
		"from_date": ["<=", today()],
		"to_date": [">=", today()]
	}, ["parent"])

	rental_orders = set()
	for row in rental_order_items:
		rental_orders.add(row.parent)

	rental_orders = list(rental_orders)

	for row in rental_orders:
		rental_order = frappe.get_doc("Rental Order", row)
		ro_exists = frappe.db.exists({
			"doctype": "Rental Timesheet",
			"date": today(),
			"docstatus": 1
		})

		if not ro_exists:
			rental_timesheet = frappe.get_doc({
				"doctype": "Rental Timesheet",
				"customer": rental_order.customer,
				"rental_order": rental_order.name,
				"company": rental_order.company,
			})

			has_items = False
			for item in rental_order.items:
				rental_assets = frappe.get_list("Rental Issue Note Item", {
												"rental_order_item": item.name
												}, ["assets"])

				qty = 0
				for row in rental_assets:
					assets = row.assets
					assets = assets.split("\n")
					for asset in assets:
						if asset:
							rental_status = frappe.get_value(
								"Asset", asset, "rental_status")
							if rental_status == "In Use":
								qty = qty + 1
				if qty:
					rental_timesheet.append("items", {
						"item_code": item.item_code,
						"qty": qty,
						"rate": item.rate,
						"asset_location": item.asset_location,
					})
					has_items = True

			if has_items:
				rental_timesheet.save()
				rental_timesheet.submit()
				frappe.db.commit()

def rental_estimation_validation():
	rental_list=frappe.db.get_list('Rental Estimation',filters={'docstatus':1},fields=['name'])
	today_date = getdate()
	for row in rental_list:
		doc = frappe.get_doc('Rental Estimation',row.name)
		if today_date > doc.valid_till :
			print('true')
			doc.set('status','Expired')
		doc.save()
	frappe.db.commit()

def rental_quotation_validation():
	rental_list=frappe.db.get_list('Rental Quotation',filters={'docstatus':1},fields=['name'])
	today_date = getdate()
	for row in rental_list:
		doc = frappe.get_doc('Rental Quotation',row.name)
		if today_date > doc.valid_till :
			print('true')
			doc.set('status','Expired')
		doc.save()
	frappe.db.commit()

def change_rental_status():
	rin = frappe.get_all("Rental Issue Note",filters={'docstatus':1,'date':[">=",today()]},fields=["name"])
	for ri in rin:
		rin_doc = frappe.get_doc("Rental Issue Note",ri.name)
		for row in rin_doc.items:
			assets = row.assets
			assets = assets.split("\n")
			for asset in assets:
				# issue date
				if asset:
					if str(rin_doc.date) <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "In transit")
						
					if str(rin_doc.rental_start_date) <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "In Use")
						frappe.db.set_value("Asset", asset, "rental_order", rin_doc.rental_order)

	rr_all = frappe.get_all("Rental Receipt",filters={'docstatus':1,'rental_stop_date':[">=",today()]},fields=["name"])
	for rr in rr_all:
		rr_doc = frappe.get_doc("Rental Receipt",rr.name)
		for row in rr_doc.items:
			assets = row.assets
			assets = assets.split("\n")
			for asset in assets:
				if asset:
					if str(rr_doc.rental_stop_date) <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "In transit")
						
					if str(rr_doc.receipt_date) <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "On hold for Inspection")
						frappe.db.set_value("Asset", asset, "rental_order", "")

	# rin = frappe.get_all("Sub Rental Issue",filters={'docstatus':1,'date':[">=",today()]},fields=["name"])
	# for ri in rin:
	# 	rin_doc = frappe.get_doc("Sub Rental Issue",ri.name)
	# 	for row in rin_doc.items:
	# 		assets = row.assets
	# 		assets = assets.split("\n")
	# 		for asset in assets:
	# 			# issue date
	# 			if asset:
	# 				if str(rin_doc.date) <= today():
	# 					frappe.db.set_value("Asset", asset, "rental_status", "In transit")
						
	# 				if str(rin_doc.rental_start_date) <= today():
	# 					frappe.db.set_value("Asset", asset, "rental_status", "In Use")
	# 					frappe.db.set_value("Asset", asset, "rental_order", rin_doc.rental_order)

	rr_all = frappe.get_all("Sub Rental Receipt",filters={'docstatus':1,'rental_start_date':[">=",today()]},fields=["name"])
	for rr in rr_all:
		rr_doc = frappe.get_doc("Sub Rental Receipt",rr.name)
		for row in rr_doc.items:
			assets = row.assets
			assets = assets.split("\n")
			for asset in assets:
				if asset:
					if str(rr_doc.rental_start_date) <= today():
						frappe.db.set_value("Asset", row.assets, "rental_status", "On hold for Inspection")
						
					if str(rr_doc.receipt_date) <= today():
						frappe.db.set_value("Asset", asset, "rental_status", "In transit")
						frappe.db.set_value("Asset", asset, "rental_order", "")

@frappe.whitelist()
def get_project(docname=None):
	if not docname:
		return 0

	proj = frappe.get_list("Project",fields = ["name"],filters = {'sub_rental_order':docname})
	if proj:
		return proj[0]
	else:
		return 0