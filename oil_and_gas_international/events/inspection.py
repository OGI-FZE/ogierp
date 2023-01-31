import frappe



@frappe.whitelist()
def create_inspection(item_code=None,warehouse=None,item_category=None):
    new_doc = frappe.new_doc('Work Order')
    new_doc.division = "Inspection"
    new_doc.skip_transfer = 1
    new_doc.date = frappe.utils.nowdate()
    new_doc.fg_warehouse = warehouse
    new_doc.production_item = item_code
    new_doc.item_category = item_category
    new_doc.bom_no = frappe.db.get_value("BOM",{"item": item_code,"inspection_bom": 1}, "name")

    new_doc.save()
    frappe.db.commit()
    return "dddddd"

