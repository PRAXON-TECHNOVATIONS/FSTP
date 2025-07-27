# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class FollowUpList(Document):
    def validate(self):
        if self.first_followup_completed:
            for row in self.followup_table:
                if row.followup_first and row.followup_first.lower() == "pending":
                    frappe.throw("You cannot mark First FollowUp Completed while any row is still 'Pending'.")

    def before_submit(self):
        for row in self.followup_table:
            if row.followup_second and row.followup_second.lower() == "pending":
                frappe.throw("You cannot submit while any FollowUp Second status is still 'Pending'.")

@frappe.whitelist()
def fetch_households_for_followup(schedule_date):
    if not schedule_date:
        return []
    schedule_date_obj = datetime.strptime(schedule_date, "%Y-%m-%d")
    start_date = schedule_date_obj
    end_date = start_date + timedelta(days=30)
    households = frappe.get_all(
        "Household Details",
        filters={
            "schedule_date": ["between", [start_date, end_date]],
        },
        fields=["name", "name_of_owner", "phone_number", "schedule_date", "address"]
    )

    return households