# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class FollowUpList(Document):
# 	pass
import frappe
from frappe.model.document import Document

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
