import frappe
from frappe import _

from ecommerce_integrations.amazon_mws import MODULE_NAME, SETTINGS_DOCTYPE


def create_ecommerce_items():
	frappe.reload_doc(MODULE_NAME, "doctype", SETTINGS_DOCTYPE)
	filters = {
		"item_group": _(
			frappe.get_single_value(SETTINGS_DOCTYPE, "item_group"),
			frappe.get_single("System Settings").language or "en",
		)
	}
	for item in frappe.db.get_all("Item", filters=filters, fields=["*"]):
		if not frappe.db.exists("Ecommerce Item", {"erpnext_item_code": item.name}):
			_create_ecommerce_item(item)


def _create_ecommerce_item(item):
	ecomm_item = frappe.new_doc("Ecommerce Item")
	ecomm_item.integration = MODULE_NAME
	ecomm_item.erpnext_item_code = item.name
	ecomm_item.integration_item_code = item.amazon_item_code
	ecomm_item.has_variants = 0
	ecomm_item.sku = item.amazon_item_code
	ecomm_item.flags.ignore_mandatory = True
	ecomm_item.save(ignore_permissions=True)
