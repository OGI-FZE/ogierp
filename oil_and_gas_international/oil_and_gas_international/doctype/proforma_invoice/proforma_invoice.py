# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.controllers.accounts_controller import get_taxes_and_charges


class ProformaInvoice(Document):
	pass

@frappe.whitelist()
def getTax(tx=None):
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Here>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
	taxes = get_taxes_and_charges('Sales Taxes and Charges Template',tx)
	return taxes