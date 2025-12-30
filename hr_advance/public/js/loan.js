
frappe.ui.form.on("Loan",{
        refresh: function(frm) {
        const dateFieldName = 'repayment_start_date';


        // Get the current date
        const today = new Date();
        const nextMonth = today.getMonth() + 1;
        const nextYear = today.getFullYear();

        const firstDayOfNextMonth = new Date(nextYear, nextMonth, 1);

        const formattedDate = [
            firstDayOfNextMonth.getFullYear(),
            (firstDayOfNextMonth.getMonth() + 1).toString().padStart(2, '0'), // getMonth() is 0-indexed, so add 1
            firstDayOfNextMonth.getDate().toString().padStart(2, '0')
        ].join('-');

        if (!frm.doc[dateFieldName]) {
            frm.set_value(dateFieldName, formattedDate);
            console.log(`Set ${dateFieldName} to: ${formattedDate}`); // For debugging in browser console
        }
    },

    applicant:function(frm){
        if (frm.doc.applicant_type == 'Employee'){
            // Check loan_product and applicant from frm.doc
            if (frm.doc.loan_product && frm.doc.applicant && frm.doc.calculate_employee_loan_amount){
                frappe.call({
                    method: "hr_advance.api.calculate_employee_loan_amount",
                    args: {
                        loan_product: frm.doc.loan_product, 
                        applicant: frm.doc.applicant, 
                        loan_eligibility_months:0,
                    },
                    callback: function (r) {
                        if (r.message) {
                            // r.message will now be the dictionary of calculated values
                            // e.g., { "loan_amount": 9000, "monthly_repayment_amount": 99 }
                            console.log(r.message); 
                            frm.set_value('loan_amount', r.message.loan_amount);
                            frm.set_value('monthly_repayment_amount', r.message.monthly_repayment_amount);
                        } else if (r.exc) { // If frappe.throw was called
                            frappe.msgprint(__("Error: {0}", [r.exc]));
                            console.error(r.exc);
                        }
                    },
                });
                frm.set_value('repayment_method', 'Repay Fixed Amount per Period');
                frm.refresh_fields();
            }
        }
    },
        loan_product:function(frm){
        if (frm.doc.applicant_type == 'Employee'){
            // Check loan_product and applicant from frm.doc
            if (frm.doc.loan_product && frm.doc.applicant && frm.doc.calculate_employee_loan_amount){
                frappe.call({
                    method: "hr_advance.api.calculate_employee_loan_amount",
                    args: {
                        loan_product: frm.doc.loan_product, 
                        applicant: frm.doc.applicant, 
                        loan_eligibility_months:0,
                    },
                    callback: function (r) {
                        if (r.message) {
                            // r.message will now be the dictionary of calculated values
                            // e.g., { "loan_amount": 9000, "monthly_repayment_amount": 99 }
                            console.log(r.message); 
                            frm.set_value('loan_amount', r.message.loan_amount);
                            frm.set_value('monthly_repayment_amount', r.message.monthly_repayment_amount);
                        } else if (r.exc) { // If frappe.throw was called
                            frappe.msgprint(__("Error: {0}", [r.exc]));
                            console.error(r.exc);
                        }
                    },
                });
                frm.set_value('repayment_method', 'Repay Fixed Amount per Period');
                frm.refresh_fields();
            }
        }
    }

});