# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ForecastDocument(Document):

	def before_insert(self):
		forecast_doc = frappe.get_list("Forecast Document",fields=["name","version"],
			filters={'fiscal_year':self.fiscal_year,'company':self.company},order_by='version')
		if forecast_doc:
			latest = forecast_doc[-1]['version']
			self.version = latest+1
		else:
			self.version = 0


