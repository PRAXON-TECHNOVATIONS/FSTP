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

    // Make followup_first read-only after checkbox is ticked AND saved
    frm.fields_dict.followup_table.grid.update_docfield_property(
        'followup_first', 'read_only', (is_checked && is_saved)
    );

    // Show followup_second only when checkbox is ticked AND saved
    frm.fields_dict.followup_table.grid.update_docfield_property(
        'followup_second', 'hidden', !(is_checked && is_saved)
    );

    frm.refresh_field('followup_table');
}

