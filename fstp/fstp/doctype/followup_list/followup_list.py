# # Copyright (c) 2025, Kapil and contributors
# # For license information, please see license.txt
# import frappe
# from frappe.model.document import Document
# from datetime import datetime, timedelta

# class FollowUpList(Document):
#     def validate(self):
#         if self.first_followup_completed:
#             for row in self.followup_table:
#                 if row.followup_first and row.followup_first.lower() == "pending":
#                     frappe.throw("You cannot mark First FollowUp Completed while any row is still 'Pending'.")

#     def before_submit(self):
#         for row in self.followup_table:
#             if row.followup_second and row.followup_second.lower() == "pending":
#                 frappe.throw("You cannot submit while any FollowUp Second status is still 'Pending'.")

# @frappe.whitelist()
# def fetch_households_for_followup(schedule_date):
#     if not schedule_date:
#         return []
#     schedule_date_obj = datetime.strptime(schedule_date, "%Y-%m-%d")
#     start_date = schedule_date_obj
#     end_date = start_date + timedelta(days=30)
#     households = frappe.get_all(
#         "Household Details",
#         filters={
#             "schedule_date": ["between", [start_date, end_date]],
#         },
#         fields=["name", "name_of_owner", "phone_number", "schedule_date", "address"]
#     )

#     return households

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta

class FollowUpList(Document):
    def __init__(self, *args, **kwargs):
        # Add a flag to prevent recursion
        self._prevent_final_status_update = False
        super().__init__(*args, **kwargs)

    def validate(self):
        if self.first_followup_completed:
            for row in self.followup_table:
                if row.followup_first and row.followup_first.lower() == "pending":
                    frappe.throw("You cannot mark First FollowUp Completed while any row is still 'Pending'.")

    def before_submit(self):
        for row in self.followup_table:
            # If the first follow-up is "Unwilling", check the second follow-up
            if row.followup_first and row.followup_first.lower() == "unwilling":
                if row.followup_second and row.followup_second.lower() == "pending":
                    frappe.throw("You cannot submit while FollowUp Second status is still 'Pending' for 'Unwilling' cases.")

            # If the first follow-up is "Pending", throw an error
            elif row.followup_first and row.followup_first.lower() == "pending":
                frappe.throw("You cannot submit while FollowUp First status is still 'Pending'.")


    def on_update(self):
        if not self._prevent_final_status_update:
            self.update_final_status()

    def update_final_status(self):
        if self._prevent_final_status_update:
            return  # Prevent recursion

        self._prevent_final_status_update = True  # Set the flag to True

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
                row.final_status = "Pending"  # or any default status you prefer

        self.save()  # Save the document after the update
        self._prevent_final_status_update = False  # Reset the flag

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
