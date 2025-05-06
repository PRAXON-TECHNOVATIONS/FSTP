// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

frappe.query_reports["Schedule Report 3"] = {
	"filters": [
		{
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"label": "Company",
		},
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "status",
			"fieldtype": "Select",
			"label": "Status",
			"options": "\nPending\nUnavailable\nUnwilling\nCompleted"
		}
	]
};