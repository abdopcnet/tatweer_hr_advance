frappe.ui.form.on('Additional Salary', {
// 	refresh(frm) {
// 		// your code here
// 	},
	set_component_query: function (frm) {
    if (!frm.doc.company) return;
    let filters = {custom_allow_it_in_monthly_variables: 1};
    // if (frm.doc.type) {
    //     filters.type = frm.doc.type;
    // }
    frm.set_query("salary_component", function () {
        return {
            filters: filters,
        };
    });
},
    custom_number_of_days : function(frm){
        if (frm.doc.custom_number_of_days > 0){
            frappe.call({
                method: "hr_advance.api.calculate_employee_base",
                args: {
                    employee: frm.doc.employee, 
                },
                callback: function (r) {
                    if (r.message) {
                        // r.message will now be the dictionary of calculated values
                        // e.g., { "loan_amount": 9000, "monthly_repayment_amount": 99 }
                        console.log(r.message); 
                        frm.set_value('amount', r.message.basic_salary / 30 * frm.doc.custom_number_of_days );
                    } else if (r.exc) { // If frappe.throw was called
                        frappe.msgprint(__("Error: {0}", [r.exc]));
                        console.error(r.exc);
                    }
                },
            });
        }
    },
})