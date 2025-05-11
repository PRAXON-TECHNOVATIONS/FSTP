# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt
# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate


class MaintenanceScheduleAndActual(Document):
    def on_submit(self):
        for row in self.scheduling_table:
            if row.status == "Completed" and row.actual_date:
                household = frappe.get_doc("Household Details", row.household_name)
                household.last_emptying_date = row.actual_date
                household.save(ignore_permissions=True)
            if row.household_name:
                frappe.db.set_value("Household Details", row.household_name, "status", "Scheduled")
        update_overdue_status()

@frappe.whitelist()
def fetch_households(schedule_date):
    if not schedule_date:
        return []
    one_week_later = add_days(schedule_date, 7)
    overdue_households = frappe.get_all("Household Details",
        filters={"status": "Overdue"},
        fields=["name", "schedule_date", "address"]
    )
    scheduled_households = frappe.get_all("Household Details",
        filters={
            "status": "Scheduled",
            "schedule_date": ["between", [schedule_date, one_week_later]]
        },
        fields=["name", "schedule_date", "address"]
    )
    combined = {h["name"]: h for h in (overdue_households + scheduled_households)}
    return list(combined.values())
def update_overdue_status():
    today = nowdate()
    overdue_households = frappe.get_all("Household Details",
        filters={"status": "Scheduled", "schedule_date": ["<", today]},
        fields=["name"]
    )
    for h in overdue_households:
        frappe.db.set_value("Household Details", h.name, "status", "Overdue")
    revert_households = frappe.get_all("Household Details",
        filters={"status": "Overdue", "schedule_date": [">=", today]},
        fields=["name"]
    )
    for h in revert_households:
        frappe.db.set_value("Household Details", h.name, "status", "Scheduled")
def on_submit(doc, method):
    for row in doc.scheduling_table:
        if row.maintenance_type == "Breakdown" and row.status == "Completed" and row.issue:
            issue = frappe.get_doc("Issue", row.issue)
            issue.status = "Resolved"
            issue.save()
            frappe.db.commit()
