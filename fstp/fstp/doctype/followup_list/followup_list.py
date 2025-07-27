# # Copyright (c) 2025, Kapil and contributors
# # For license information, please see license.txt
import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class FollowUpList(Document):
    def __init__(self, *args, **kwargs):
        self._prevent_final_status_update = False
        super().__init__(*args, **kwargs)

    def validate(self):
        if self.first_followup_completed:
            for row in self.followup_table:
                if row.followup_first and row.followup_first.lower() == "pending":
                    frappe.throw("You cannot mark First FollowUp Completed while any row is still 'Pending'.")

    def before_submit(self):
        for row in self.followup_table:
            if row.followup_first and row.followup_first.lower() == "unwilling":
                if row.followup_second and row.followup_second.lower() == "pending":
                    frappe.throw("You cannot submit while FollowUp Second status is still 'Pending' for 'Unwilling' cases.")
            elif row.followup_first and row.followup_first.lower() == "pending":
                frappe.throw("You cannot submit while FollowUp First status is still 'Pending'.")


    def on_update(self):
        if not self._prevent_final_status_update:
            self.update_final_status()

    def update_final_status(self):
        if self._prevent_final_status_update:
            return

        self._prevent_final_status_update = True

        for row in self.followup_table:
            if row.followup_first:
                if row.followup_first.lower() == "available":
                    row.final_status = "Available"
                elif row.followup_first.lower() == "unavailable":
                    row.final_status = "Unavailable"
                elif row.followup_first.lower() == "unwilling" and row.followup_second:
                    if row.followup_second.lower() == "available":
                        row.final_status = "Available"
                    elif row.followup_second.lower() == "unavailable":
                        row.final_status = "Unavailable"
                    elif row.followup_second.lower() == "unwilling":
                        row.final_status = "Unwilling"
            else:
                row.final_status = "Pending"

        self.save()
        self._prevent_final_status_update = False

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

@frappe.whitelist()
def make_final_list(followup_list_name):
    followup_list = frappe.get_doc('FollowUp List', followup_list_name)
    if not followup_list:
        return "FollowUp List not found!"
    
    final_list_doc = frappe.new_doc('Final List')
    final_list_doc.update({
        'title': f"Final List for {followup_list_name}",
        'followup_list': followup_list_name,
        'schedule_date': followup_list.schedule_date,
    })
    for row in followup_list.followup_table:
        if row.final_status == "Available":
            final_list_row = final_list_doc.append('final_table', {
                'household_owner': row.household,
            })
    
    final_list_doc.insert()
    followup_list.custom_final_list_created = True
    followup_list.save()

    return "success"
