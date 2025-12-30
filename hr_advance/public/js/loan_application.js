
frappe.ui.form.on("Loan Application",{

    
    applicant:function(frm){
        if (frm.doc.applicant_type == 'Employee'){
            // Check loan_product and applicant from frm.doc
            if (frm.doc.loan_product && frm.doc.applicant && frm.doc.custom_loan_eligibility_months){
                frappe.call({
                    method: "hr_advance.api.calculate_employee_loan_amount",
                    args: {
                        loan_product: frm.doc.loan_product, 
                        applicant: frm.doc.applicant, 
                        loan_eligibility_months :frm.doc.custom_loan_eligibility_months,
                    },
                    callback: function (r) {
                        if (r.message) {
                            // r.message will now be the dictionary of calculated values
                            // e.g., { "loan_amount": 9000, "monthly_repayment_amount": 99 }
                            console.log(r.message); 
                            frm.set_value('loan_amount', r.message.basic_salary * frm.doc.custom_loan_eligibility_months);
                            frm.set_value('repayment_amount', r.message.monthly_repayment_amount);
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
        if (frm.doc.loan_product && frm.doc.applicant && frm.doc.custom_loan_eligibility_months){
            frappe.call({
                method: "hr_advance.api.calculate_employee_loan_amount",
                args: {
                    loan_product: frm.doc.loan_product, 
                    applicant: frm.doc.applicant, 
                    loan_eligibility_months :0,
                },
                callback: function (r) {
                    if (r.message) {
                        // r.message will now be the dictionary of calculated values
                        // e.g., { "loan_amount": 9000, "monthly_repayment_amount": 99 }
                        console.log(r.message); 
                        frm.set_value('loan_amount', r.message.basic_salary * frm.doc.custom_loan_eligibility_months);
                        frm.set_value('repayment_amount', r.message.monthly_repayment_amount);
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
    custom_loan_eligibility_months:function(frm){
        if (frm.doc.applicant_type == 'Employee'){
            // Check loan_product and applicant from frm.doc
            if (frm.doc.loan_product && frm.doc.applicant && frm.doc.custom_loan_eligibility_months){
                frappe.call({
                    method: "hr_advance.api.calculate_employee_loan_amount",
                    args: {
                        loan_product: frm.doc.loan_product, 
                        applicant: frm.doc.applicant, 
                        loan_eligibility_months :frm.doc.custom_loan_eligibility_months,
                    },
                    callback: function (r) {
                        if (r.message) {
                            // r.message will now be the dictionary of calculated values
                            // e.g., { "loan_amount": 9000, "monthly_repayment_amount": 99 }
                            console.log(r.message); 
                            frm.set_value('loan_amount', r.message.basic_salary * frm.doc.custom_loan_eligibility_months);
                            frm.set_value('repayment_amount', r.message.monthly_repayment_amount);
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
    status:function(frm){
        // console.log("testttttttttttttttttttt")
        if (frm.doc.status == "Approved"){
            if (!frm.doc.custom_works_for_more_than_1_year){
                frm.set_value('status', 'Open');
                frappe.throw(__('Can not change Status to Approved while the works for more than 1 year is not checked'))
                
            }
            if (!frm.doc.custom_regular_attendance){
                frm.set_value('status', 'Open');
                frappe.throw(__('Can not change Status to Approved while the Regular Attendance is not checked'))
            }
            if (!frm.doc.custom_performance_rating_at_least_good){
                frm.set_value('status', 'Open');
                frappe.throw(__('Can not change Status to Approved while the Performance Rating at least Good is not checked'))
            }
            if (!frm.doc.custom_bank_statement_provided){
                frm.set_value('status', 'Open');
                frappe.throw(__('Can not change Status to Approved while the Bank Statement Providedis not checked'))
            }
            if (!frm.doc.custom_last_loan_installment_over_2_years_ago){
                frm.set_value('status', 'Open');
                frappe.throw(__('Can not change Status to Approved while the Last Loan Installment over 2 years ago is not checked'))
            }
            // if (!frm.doc.custom_promissory_note_received){
            //     frm.set_value('status', 'Open');
            //     frappe.throw(__('Can not change Status to Approved while the Promissory Note Received is not checked'))
            // }
            if (!frm.doc.custom_has_financial_coverage){
                frm.set_value('status', 'Open');
                frappe.throw(__('Can not change Status to Approved while the Has Financial Coverage is not checked'))
            }

        }
    },
    before_submit : function(frm){
        if (frm.doc.status != "Approved"){
            frappe.throw(__('Can not subbmit the document while the status not approved'))

    }},


});