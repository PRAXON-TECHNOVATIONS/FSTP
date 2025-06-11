// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Issue", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Issue', {
    refresh: function (frm) {
        if (!frm.is_new() && frm.doc.status === "Open") {
            frm.add_custom_button('Add to Schedule', () => {
                frappe.call({
                    method: "fstp.fstp.doctype.issue.issue.add_to_latest_schedule",
                    args: {
                        issue_date: frm.doc.creation,
                        household: frm.doc.household,
                        issue_name: frm.doc.name
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint({
                                title:("Scheduled"),
                                message: `Issue has been scheduled in <b>${r.message.schedule_name}</b> on <b>${r.message.schedule_date}</b>.`,
                                indicator: 'green'
                            });
                            frm.reload_doc();
                        } else {
                            frappe.msgprint({
                                title:("Not Found"),
                                message: "No draft maintenance schedule found.",
                                indicator: 'orange'
                            });
                        }
                    }
                });
            });
        }
    }
});
