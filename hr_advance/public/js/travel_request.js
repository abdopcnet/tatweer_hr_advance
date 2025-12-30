frappe.ui.form.on('Travel Request', {
    refresh: function(frm) {
        // Add the button only if the Travel Request is submitted
        if (frm.doc.docstatus === 1) { // 1 means Submitted
            frm.add_custom_button(__('Create Expense Claim'), function() {
                // Confirm with the user before proceeding
                frappe.confirm(
                    __('Are you sure you want to create an Expense Claim from this Travel Request?'),
                    function() { // On confirmation
                        // Call a server-side method to create the Expense Claim
                        frappe.call({
                            method: "hr_advance.api.create_expense_claim_from_travel_request",
                            args: {
                                travel_request_name: frm.doc.name
                            },
                            callback: function(r) {
                                if (r.message) {
                                    // r.message will contain the name of the newly created Expense Claim
                                    frappe.msgprint(__('Expense Claim {0} created successfully.', [r.message]));
                                    // Redirect to the new Expense Claim form
                                    frappe.set_route("Form", "Expense Claim", r.message);
                                } else if (r.exc) {
                                    frappe.msgprint({
                                        title: __('Error'),
                                        message: __('Failed to create Expense Claim: {0}', [r.exc]),
                                        indicator: 'red'
                                    });
                                }
                            }
                        });
                    },
                    function() { // On cancel
                        frappe.msgprint(__('Expense Claim creation cancelled.'));
                    }
                );
            }, ); 
        }
    }
});