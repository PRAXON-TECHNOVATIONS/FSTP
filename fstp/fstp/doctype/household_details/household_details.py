# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import timedelta

class HouseholdDetails(Document):
	def on_update(self):
		if self.last_emptying_date:
			last_date = frappe.utils.get_datetime(self.last_emptying_date)
			next_date = last_date + timedelta(days=365)
			if self.schedule_date != next_date.date():
				self.schedule_date = next_date.date()
				self.save()