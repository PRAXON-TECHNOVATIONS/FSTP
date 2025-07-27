// Copyright (c) 2025, Kapil and contributors
// For license information, please see license.txt

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

    schedule_date: function(frm) {
        fetch_households_based_on_dates(frm);
    },

    after_save: function(frm) {
        setTimeout(() => {
            apply_followup_logic(frm);
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
    frm.fields_dict.followup_table.grid.update_docfield_property(
        'followup_first', 'read_only', (is_checked && is_saved)
    );
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
    frm.fields_dict.followup_table.grid.refresh_row(row.idx - 1);
}
function fetch_households_based_on_dates(frm) {
    if (frm.doc.schedule_date) {
        frappe.call({
            method: 'fstp.fstp.doctype.followup_list.followup_list.fetch_households_for_followup',
            args: {
                schedule_date: frm.doc.schedule_date
            },
            callback: function(r) {
                if (r.message) {
                    frm.clear_table('followup_table');
                    r.message.forEach(function(row) {
                        let child = frm.add_child('followup_table');
                        child.household = row.name;
                        child.household_name = row.name_of_owner; 
                        child.address = row.address;
                        child.phone_number = row.phone_number;
                    });
                    frm.refresh_field('followup_table');
                }
            }
        });
    }
}


