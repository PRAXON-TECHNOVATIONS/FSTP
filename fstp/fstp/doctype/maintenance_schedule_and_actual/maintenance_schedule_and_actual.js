// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Schedule And Actual', {
    schedule_date: function(frm) {
        if (frm.doc.schedule_date) {
            frappe.call({
                method: 'fstp.fstp.doctype.maintenance_schedule_and_actual.maintenance_schedule_and_actual.fetch_households',
                args: {
                    schedule_date: frm.doc.schedule_date
                },
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table('scheduling_table');
                        r.message.forEach(function(row) {
                            let child = frm.add_child('scheduling_table');
                            child.household_name = row.name;
                            child.schedule_date = row.schedule_date;
                            child.address = row.address;
                        });
                        frm.refresh_field('scheduling_table');
                    }
                }
            });
        }
    },

    onload: function(frm) {
        // Attach the issue field filter logic for child rows
        frm.fields_dict.scheduling_table.grid.get_field('issue').get_query = function(doc, cdt, cdn) {
            const child = locals[cdt][cdn];
            if (child.maintenance_type === "Breakdown") {
                return {
                    filters: {
                        status: "Open"
                    }
                };
            } else {
                // Optional: restrict or allow all when not Breakdown
                return {
                    filters: {}
                };
            }
        };
    }
});

// Also handle refresh of the issue field when maintenance_type changes
frappe.ui.form.on('MaintenanceScheduleChild', {
    maintenance_type: function(frm, cdt, cdn) {
        const child = locals[cdt][cdn];
        // Re-evaluate issue query filter
        frappe.meta.get_docfield("MaintenanceScheduleChild", "issue", frm.doc.name).get_query = function() {
            if (child.maintenance_type === "Breakdown") {
                return {
                    filters: {
                        status: "Open"
                    }
                };
            } else {
                return {
                    filters: {}
                };
            }
        };
    }
});
