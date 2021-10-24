# -*- coding: utf-8 -*-
# Copyright (c) 2020, Havenir Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AssetFormation(Document):
	def on_submit (self):
		self.db_set('status', 'Submitted')
	
	def create_assets (self):
		'''
		`(doc) --> None`
		creates new assets in draft mode
		'''
		for row in self.items:
			asset_doc = frappe.new_doc('Asset')
			asset_doc.company = self.company
			asset_doc.asset_name = row.serial_no
			asset_doc.item_code = self.asset_item_code
			asset_doc.location = row.location
			asset_doc.asset_owner = 'Company'
			asset_doc.purchase_date = row.creation_date
			asset_doc.is_existing_asset = 1
			asset_doc.against_asset_formation = self.name
			asset_doc.customer = row.customer
			asset_doc.project = row.project

			# getting valuation rate for the item
			value = frappe.get_value('Bin', 
			{
				'item_code' : self.item_code,
				'warehouse': self.warehouse
			}, ['valuation_rate'])

			asset_doc.gross_purchase_amount = value

			asset_doc.insert()

			self.db_set('status', 'Assets in Draft Mode')
			

			
