import frappe
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()
def make_estimation(source_name, target_doc=None):
	doclist = get_mapped_doc("Opportunity", source_name, {
			"Opportunity": {
				"doctype": "Estimation Sheet",
				"field_map": {
					"name" : "opportunity"
				}
			},
			"Opportunity Item": {
				"doctype": "Estimation Sheet Item",
				"field_map": {
					"item_code": "item_code",
					"description_2":"description_2",
                    "customer_requirement":"customer_requirement"
				},
			}
		}, target_doc)

	return doclist

@frappe.whitelist()
def get_lost_and_damage_prices(item_code='TESTING'):
    if not item_code:
        return 0, 0

    lihdbr = 0
    oprunning = 0
    standby = 0
    redress = 0
    straight = 0
    post_rental_inspection_charges = 0

    rd_settings = frappe.get_single("Rental Division Settings")

    if rd_settings.lih_dbr:
        lihdbr = frappe.get_value("Item Price", {
            "price_list": rd_settings.lih_dbr,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.operational_running:
        oprunning = frappe.get_value("Item Price", {
            "price_list": rd_settings.operational_running,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.standby:
        standby = frappe.get_value("Item Price", {
            "price_list": rd_settings.standby,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.redress:
        redress = frappe.get_value("Item Price", {
            "price_list": rd_settings.redress,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.straight:
        straight = frappe.get_value("Item Price", {
            "price_list": rd_settings.straight,
            "item_code": item_code
        }, "price_list_rate")

    if rd_settings.post_rental_inspection_charges:
        post_rental_inspection_charges = frappe.get_value("Item Price", {
            "price_list": rd_settings.post_rental_inspection_charges,
            "item_code": item_code
        }, "price_list_rate")

    return oprunning, standby , lihdbr, redress, straight, post_rental_inspection_charges

@frappe.whitelist()
def get_sales_person_details(sp = None):
    if not sp:
        return []
    mobile = ''
    mail_id = ''
    sp_name = ''
    sp_doc = frappe.get_doc("Sales Person",sp)
    if sp_doc.employee:
        emp_doc = frappe.get_doc("Employee",sp_doc.employee)
        mobile = emp_doc.cell_number
        mail_id = emp_doc.company_email
        sp_name = emp_doc.employee_name
    return mobile,mail_id,sp_name

@frappe.whitelist()
def get_estimation(opp=None):
    opportunity = frappe.get_doc("Opportunity",opp)
    est = frappe.get_all("Estimation Sheet",{"opportunity":opp,"docstatus":1})
    if est:
        return est[0].name


