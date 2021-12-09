# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt


import frappe
import dateutil
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from ecommerce_integrations.amazon_mws.amazon_methods import get_orders


class AmazonMWSSettings(Document):
	def validate(self):
		if self.enable_amazon == 1:
			self.enable_sync = 1
			setup_custom_fields()
		else:
			self.enable_sync = 0

	@frappe.whitelist()
	def get_products_details(self):
		if self.enable_amazon == 1:
			frappe.enqueue('ecommerce_integrations.amazon_mws.amazon_methods.get_products_details')

	@frappe.whitelist()
	def get_order_details(self):
		if self.enable_amazon == 1:
			after_date = dateutil.parser.parse(self.after_date).strftime("%Y-%m-%d")
			frappe.enqueue('ecommerce_integrations.amazon_mws.amazon_methods.get_orders', after_date=after_date)

def schedule_get_order_details():
	mws_settings = frappe.get_doc("Amazon MWS Settings")
	if mws_settings.enable_sync and mws_settings.enable_amazon:
		after_date = dateutil.parser.parse(mws_settings.after_date).strftime("%Y-%m-%d")
		get_orders(after_date = after_date)

def setup_custom_fields():
	custom_fields = {
		"Item": [dict(fieldname='amazon_item_code', label='Amazon Item Code',
			fieldtype='Data', insert_after='series', read_only=1, print_hide=1)],
		"Sales Order": [dict(fieldname='amazon_order_id', label='Amazon Order ID',
			fieldtype='Data', insert_after='title', read_only=1, print_hide=1)]
	}

	create_custom_fields(custom_fields)
