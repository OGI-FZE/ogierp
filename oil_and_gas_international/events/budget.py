import frappe
from frappe import _

def validate(doc,method):
    if doc.accounts:
        tot_budget_amount = 0
        net_amount = 0
        for i in doc.accounts:
            tot_budget_amount = tot_budget_amount + i.budget_amount
    if doc.custom_budget_details:
        for i in doc.custom_budget_details:
            net_amount = net_amount + i.amount
    if tot_budget_amount != net_amount:
        frappe.throw(_("Buget amount should be equal to budget details amount"), title=_("Cannot Save"))
