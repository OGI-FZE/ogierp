import frappe



@frappe.whitelist()
def create_inspection(item_code=None,warehouse=None,item_category=None):
    new_doc = frappe.new_doc('Inspection')
    new_doc.item_code = item_code
    new_doc.warehouse = warehouse
    new_doc.item_category = item_category
    new_doc.save()
    frappe.db.commit()
    return "dddddd"

