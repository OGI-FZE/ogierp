import frappe


def check_validity():
    pass


@frappe.whitelist()
def get_opportunity_items(docname=None):
    if not docname:
        return []

    filters = {"parent": docname}
    items = frappe.get_list("Opportunity Item", filters, ["*"])
    return items
