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
            if row.household_name:
                try:
                    household_doc = frappe.get_doc("Household Details", row.household_name)
                except frappe.DoesNotExistError:
                    continue
                schedule_date = row.schedule_date
                already_logged = any(
                    log.schedule_date == schedule_date
                    and log.maintenance_type == row.maintenance_type
                    and (log.issue == row.issue if row.issue else True)
                    for log in household_doc.maintenance_log
                )
                if not already_logged:
                    household_doc.append("maintenance_log", {
                        "household_name": row.household_name,
                        "schedule_date": schedule_date,
                        "actual_date": row.actual_date if row.status == "Completed" else None,
                        "issue": row.issue or None,
                        "status": row.status or "Pending",
                        "maintenance_type": row.maintenance_type
                    })
                    household_doc.save(ignore_permissions=True)

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
        if row.actual_date and row.status != "Completed":
            frappe.throw(f"Row for household '{row.household_name}' has an Actual Date set, so status must be 'Completed'.")
        if row.maintenance_type == "Breakdown" and row.status == "Completed" and row.issue:
            try:
                issue = frappe.get_doc("Issue", row.issue)
                if issue.status != "Resolved":
                    issue.status = "Resolved"
                    issue.actual_date = row.actual_date
                    issue.save(ignore_permissions=True)
                    frappe.db.commit()
            except frappe.DoesNotExistError:
                pass


