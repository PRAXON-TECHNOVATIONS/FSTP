# # Copyright (c) 2025, Kapil and contributors
# # For license information, please see license.txt

# # import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

# import frappe

# def execute(filters=None):
#     columns = [
#         {"label": "Name", "fieldname": "name", "fieldtype": "Data", "width": 120},
#         {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 120},
#         {"label": "Phone Number", "fieldname": "phone_number", "fieldtype": "Phone", "width": 120},
#         {"label": "Schedule Date", "fieldname": "schedule_date", "fieldtype": "Date", "width": 120},
#         {"label": "Status", "fieldname": "status", "fieldtype": "Select", "options": "\nPending\nUnavailable\nUnwilling\nCompleted", "width": 120},
#         {"label": "Household Name", "fieldname": "household_name", "fieldtype": "Data", "width": 120},
#         {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 120},
#     ]

#     data = frappe.db.sql("""
#         SELECT
#             parent.name,
#             parent.company,
#             child.phone_number,
#             child.schedule_date,
#             child.status,
#             child.household_name,
#             child.address
#         FROM
#             `tabMaintenance Schedule Child` AS child
#         INNER JOIN
#             `tabMaintenance Schedule And Actual` AS parent
#             ON child.parent = parent.name
#         ORDER BY
#             parent.modified DESC
#         LIMIT 20
#     """, as_dict=True)

#     return columns, data


import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # Prepare conditions and values for SQL query
    conditions = []
    values = {}

    if filters.get("company"):
        conditions.append("parent.company = %(company)s")
        values["company"] = filters["company"]

    if filters.get("from_date"):
        conditions.append("child.schedule_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("child.schedule_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    if filters.get("status"):
        conditions.append("child.status = %(status)s")
        values["status"] = filters["status"]

    # Construct the WHERE clause
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    # Define the columns
    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Data", "width": 120},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 120},
        {"label": "Phone Number", "fieldname": "phone_number", "fieldtype": "Phone", "width": 120},
        {"label": "Schedule Date", "fieldname": "schedule_date", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Select", "options": "\nPending\nUnavailable\nUnwilling\nCompleted", "width": 120},
        {"label": "Household Name", "fieldname": "household_name", "fieldtype": "Data", "width": 120},
        {"label": "Address", "fieldname": "address", "fieldtype": "Data", "width": 120},
    ]

    # SQL query with filters applied
    query = f"""
        SELECT
            parent.name,
            parent.company,
            child.phone_number,
            child.schedule_date,
            child.status,
            child.household_name,
            child.address
        FROM
            `tabMaintenance Schedule Child` AS child
        INNER JOIN
            `tabMaintenance Schedule And Actual` AS parent
            ON child.parent = parent.name
        {where_clause}
        ORDER BY
            parent.modified DESC
        LIMIT 100
    """

    data = frappe.db.sql(query, values, as_dict=True)

    return columns, data