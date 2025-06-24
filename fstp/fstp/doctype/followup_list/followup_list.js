// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

// frappe.ui.form.on("FollowUp List", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('FollowUp List', {
    onload: function(frm) {
        apply_followup_logic(frm);
    },

    refresh: function(frm) {
        apply_followup_logic(frm);
    },

    first_followup_completed: function(frm) {
        apply_followup_logic(frm);
    },

    after_save: function(frm) {
        apply_followup_logic(frm);
    }
});

function apply_followup_logic(frm) {
    const is_checked = frm.doc.first_followup_completed === 1;
    const is_saved = !frm.is_new();

    // Show/hide followup_second column
    frm.fields_dict.scheduling_table.grid.update_docfield_property(
        'followup_second', 'hidden', !(is_checked && is_saved)
    );

    frm.fields_dict.scheduling_table.grid.grid_rows.forEach(row => {
        if (is_checked && is_saved) {
            // Freeze followup_first
            row.toggle_editable('followup_first', false);
        } else {
            // Make it editable again if needed
            row.toggle_editable('followup_first', true);
        }
    });

    frm.refresh_field('scheduling_table');
}
