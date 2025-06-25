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
        // Run logic after short delay to ensure field refresh
        setTimeout(() => {
            apply_followup_logic(frm);

            // ✅ Freeze checkbox only after save, not before
            const is_checked = frm.doc.first_followup_completed === 1;
            const all_first_done = (frm.doc.followup_table || []).every(row =>
                row.followup_first && row.followup_first !== "Pending"
            );

            if (is_checked && all_first_done) {
                frm.set_df_property("first_followup_completed", "read_only", 1);
            }

            frm.fields_dict.followup_table.grid.refresh();
        }, 300);
    }
});

frappe.ui.form.on('FollowUp Table', {
    followup_first: function(frm, cdt, cdn) {
        handle_followup_second_visibility(frm, cdt, cdn);
    }
});

function apply_followup_logic(frm) {
    const is_checked = frm.doc.first_followup_completed === 1;
    const is_saved = !frm.is_new();

    // 1. Make followup_first read-only after checkbox is ticked AND saved
    frm.fields_dict.followup_table.grid.update_docfield_property(
        'followup_first', 'read_only', (is_checked && is_saved)
    );

    // 2. Apply row-wise logic for followup_second visibility
    (frm.doc.followup_table || []).forEach(row => {
        handle_followup_second_visibility(frm, row.doctype, row.name);
    });

    frm.refresh_field('followup_table');
    frm.refresh_field('first_followup_completed');
}

function handle_followup_second_visibility(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    const parent_checked = frm.doc.first_followup_completed === 1;
    const show_second = parent_checked &&
        (row.followup_first === "Unwilling" || row.followup_first === "Unavailable");

    frappe.meta.get_docfield("FollowUp Table", "followup_second", frm.doc.name).hidden = !show_second;

    // Refresh only that row
    frm.fields_dict.followup_table.grid.refresh_row(row.idx - 1);
}



