# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import timedelta
from frappe.utils import nowdate, get_datetime, getdate

class HouseholdDetails(Document):
    def on_update(self):
        if self.last_emptying_date:
            last_date = get_datetime(self.last_emptying_date)
            next_date = last_date + timedelta(days=365)
            if self.schedule_date != next_date.date():
                self.schedule_date = next_date.date()
                self.save()

    def validate(self):
        today = getdate(nowdate())

        if self.schedule_date:
            schedule_date = getdate(self.schedule_date)

            if schedule_date < today:
                self.status = "Overdue"
            else:
                self.status = "Scheduled"


def mark_overdue_households():
    today = nowdate()

    overdue_households = frappe.get_all("HouseHold Details",
        filters={
            "schedule_date": ("<", today),
            "status": ("!=", "Overdue")
        },
        fields=["name"]
    )

    count_overdue = 0
    for household in overdue_households:
        doc = frappe.get_doc("HouseHold Details", household.name)
        doc.status = "Overdue"
        doc.save(ignore_permissions=True)
        count_overdue += 1

    upcoming_households = frappe.get_all("HouseHold Details",
        filters={
            "schedule_date": (">=", today),
            "status": ("!=", "Scheduled")
        },
        fields=["name"]
    )

    count_scheduled = 0
    for household in upcoming_households:
        doc = frappe.get_doc("HouseHold Details", household.name)
        doc.status = "Scheduled"
        doc.save(ignore_permissions=True)
        count_scheduled += 1

    frappe.logger().info(f"[HouseHold Details] Marked {count_overdue} as Overdue, {count_scheduled} as Scheduled")
