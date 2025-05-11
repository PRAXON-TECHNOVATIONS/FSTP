// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Maintenance Schedule And Actual", {
// 	refresh(frm) {

// 	},
// });
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
    }
});
