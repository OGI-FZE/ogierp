import frappe
from frappe import _


@frappe.whitelist()
def create_inspection(qty,item_code,warehouse=None,item_category=None,project=None,project_wo=None,sales_o=None,rental_o=None):
    new_doc = frappe.new_doc('Work Order')
    if float(qty) == 0:
        frappe.throw(_("You don't have Item : {} in warehouse {}")
                    .format(item_code,warehouse))
    else:
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
        new_doc.bom_no = frappe.db.get_value("BOM",{"item": item_code,"inspection_bom": 1}, "name")
        new_doc.save()
        frappe.db.commit()
    return "dddddd"

