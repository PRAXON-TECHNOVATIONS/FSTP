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
                method: "fstp.fstp.doctype.maintenance_schedule_and_actual.maintenance_schedule_and_actual.get_households_by_date",
                args: {
                    schedule_date: frm.doc.schedule_date
                },
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table("scheduling_table");
                        r.message.forEach(function(household) {
                            let row = frm.add_child("scheduling_table");
                            row.household_name = household.name;
                            row.phone_number = household.phone_number;
                            row.address = household.address;
                            row.schedule_date = household.schedule_date;
                        });
                        frm.refresh_field("scheduling_table");
                    }
                }
            });
        }
    }
});
