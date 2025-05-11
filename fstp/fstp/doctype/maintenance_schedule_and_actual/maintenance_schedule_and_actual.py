# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaintenanceScheduleAndActual(Document):
    def on_submit(self):
        for row in self.scheduling_table:
            if row.status == "Completed" and row.actual_date:
                household = frappe.get_doc("Household Details", row.household_name)
                household.last_emptying_date = row.actual_date
                household.save(ignore_permissions=True)

@frappe.whitelist()
def get_households_by_date(schedule_date):
    households = frappe.get_all("Household Details",
        filters={"schedule_date": schedule_date},
        fields=["name", "phone_number", "address", "schedule_date"]
    )
    return households

def on_submit(doc, method):
    for row in doc.scheduling_table:
        if row.maintenance_type == "Breakdown" and row.status == "Completed" and row.issue:
            issue = frappe.get_doc("Issue", row.issue)
            issue.status = "Resolved"
            issue.save()
            frappe.db.commit()
