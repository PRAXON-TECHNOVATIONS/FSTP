# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class Issue(Document):
	pass

@frappe.whitelist()
def add_to_latest_schedule(issue_date, household, issue_name):
    if not (issue_date and household and issue_name):
        frappe.throw("Issue date, household, and issue name are required.")
    try:
        issue_date = datetime.strptime(issue_date, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        issue_date = datetime.strptime(issue_date, "%Y-%m-%d %H:%M:%S")
    issue = frappe.get_doc("Issue", issue_name)
    if issue.status in ["Scheduled", "Resolved"]:
        return
    latest_schedule = frappe.get_all(
        "Maintenance Schedule And Actual",
        filters={"docstatus": 0},
        fields=["name", "schedule_date"],
        order_by="creation desc",
        limit=1
    )
    if not latest_schedule:
        return
    schedule_doc = frappe.get_doc("Maintenance Schedule And Actual", latest_schedule[0].name)
    if not any(row.household_name == household and row.issue == issue_name for row in schedule_doc.scheduling_table):
        schedule_doc.append("scheduling_table", {
            "household_name": household,
            "maintenance_type": "Breakdown",
            "issue": issue_name
        })
        schedule_doc.save(ignore_permissions=True)
        frappe.db.commit()
        issue.status = "Scheduled"
        issue.save(ignore_permissions=True)
        frappe.db.commit()
    return {
        "schedule_name": schedule_doc.name,
        "schedule_date": str(schedule_doc.schedule_date)
    }

def validate(doc, method):
    if doc.status == "Open" and frappe.db.get_value("Issue", doc.name, "status") == "Resolved":
        frappe.throw("You cannot reopen a resolved Issue.")

def on_submit(doc, method=None):
    for row in doc.scheduling_table:
        if row.status == "Completed" and row.issue:
            issue = frappe.get_doc("Issue", row.issue)
            if issue.status != "Resolved":
                issue.status = "Resolved"
                issue.save(ignore_permissions=True)
