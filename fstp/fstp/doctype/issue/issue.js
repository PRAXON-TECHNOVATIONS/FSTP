// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

frappe.ui.form.on('Issue', {
    refresh: function(frm) {
        if (frm.doc.status === 'Open') {
            frm.add_custom_button(__('Add to Final List'), function() {
                if (!frm.doc.household) {
                    frappe.msgprint(__('Please provide a household.'));
                    return;
                }
                frappe.call({
                    method: 'fstp.fstp.doctype.issue.issue.add_to_final_list',
                    args: {
                        issue_name: frm.doc.name,
                        household: frm.doc.household
                    },
                    callback: function(response) {
                        frappe.msgprint(response.message);
                    },
                    error: function(err) {
                        frappe.msgprint(__('Error while adding to Final List.'));
                    }
                });
            });
        }
    }
});
