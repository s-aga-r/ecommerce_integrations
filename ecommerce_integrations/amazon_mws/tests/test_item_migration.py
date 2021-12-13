import unittest

import frappe
from frappe import _

from ecommerce_integrations.amazon_mws.constants import MODULE_NAME, SETTINGS_DOCTYPE
from ecommerce_integrations.patches.update_amazon_mws_items import create_ecommerce_items


class TestAmazonMWSItemMigration(unittest.TestCase):
	def test_migrate_items(self):
		create_ecommerce_items()
		filters = {
			"item_group": _(
				frappe.get_single_value(SETTINGS_DOCTYPE, "item_group"),
				frappe.get_single("System Settings").language or "en",
			)
		}
		items_count = frappe.db.count("Item", filters)
		ecomm_items_count = frappe.db.count("Ecommerce Item", {"integration": MODULE_NAME})
		self.assertEqual(items_count, ecomm_items_count)
