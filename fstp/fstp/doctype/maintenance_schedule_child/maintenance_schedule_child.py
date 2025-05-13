# Copyright (c) 2025, Kapil and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


frappe.ui.form.on('Maintenance Schedule And Actual', {
    onload: function(frm) {
        frm.fields_dict.scheduling_table.grid.get_field('issue').get_query = function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
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

