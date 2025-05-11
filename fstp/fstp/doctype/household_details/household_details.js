// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Household Details", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Household Details', {
    last_emptying_date: function(frm) {
        if (frm.doc.last_emptying_date) {
            let lastDate = frappe.datetime.str_to_obj(frm.doc.last_emptying_date);
            let nextDate = frappe.datetime.add_days(lastDate, 365); // Adds 1 year
            frm.set_value('schedule_date', frappe.datetime.obj_to_str(nextDate));
        }
    }
});
