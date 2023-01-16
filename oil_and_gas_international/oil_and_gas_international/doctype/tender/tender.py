# Copyright (c) 2022, Havenir Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Tender(Document):
	def validate(self):
		if  self.is_new():
		    self.copy_from_template()
		else:
			self.set("activities", [])
			self.copy_from_template()



	def copy_from_template(self):
		"""
		Copy activity from template
		# """
		if self.template:
			template_doc = frappe.get_doc('Tender Template',self.template)
			for row in template_doc.activities:
				if row.activity in self.activities:
					pass
				else:
					self.append('activities', {
						'tender_activity': row.activity,
					})

		# if self.template and not frappe.db.get_all("Tender Activity", dict(tender=self.name), limit=1):

		# 	# has a template, and no loaded activities, so lets create
		# 	if not self.date:
		# 		# tender starts today
		# 		self.date = today()

		# 	template = frappe.get_doc("Tender Template", self.template)

		# 	if not self.type:
		# 		self.type = template.tender_type

		# 	# create activity from template
		# 	tender_activities = []
		# 	tmp_act_details = []
		# 	for activity in template.activities:
		# 		template_act_details = frappe.get_doc("Tender Activity", activity.activity)
		# 		tmp_act_details.append(template_act_details)
		# 		activity = self.create_activity_from_template(template_act_details)
		# 		tender_activities.append(activity)

		# 	for act in tender_activities:
		# 		self.append('activities',
		# 			{
		# 				'tender_activity':act.name, 
		# 	            'assigned_to': act.assigned_to, 
		# 	            'status': act.status,
		# 	            'parent':self.name
		# 			}
		# 		)
			# self.save()

	def create_activity_from_template(self, activity_details):
		return frappe.get_doc(
			dict(
				doctype="Tender Activity",
				name1=activity_details.name1,
				tender=self.name,
				status="Open",
			)
		).insert()

	def after_insert(self):
		self.copy_from_template()