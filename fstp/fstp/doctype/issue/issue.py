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
def add_to_final_list(issue_name, household):
    final_list = frappe.get_all(
        'Final List', 
        filters={'docstatus': 0},
        fields=['name']
    )

    if final_list:
        final_list_doc = frappe.get_doc('Final List', final_list[0].name)
        new_row = {
            'household_owner': household,
            'maintenance_type': 'Complaint',
            'issue': issue_name
        }
        final_list_doc.append('final_table', new_row)
        final_list_doc.save()

        return ('Household added to the first Draft Final List successfully.')

    else:
        return ('No Draft Final List found.')