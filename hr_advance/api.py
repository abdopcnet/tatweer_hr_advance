import re
import frappe
from datetime import date
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, today
from frappe.utils.data import money_in_words
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import getdate

import erpnext
import re

#
# this code work in employee fileds for bank branches

@frappe.whitelist()
def fetch_bank_branch_list(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """
        SELECT branch_name
        FROM `tabEmployee Bank Branch`
        WHERE parent = %(bank_name)s
		and `branch_name` LIKE %(txt)s
        """.format(
            key=searchfield
        ),
        {
            "txt": "%%%s%%" % txt,
            "start": start,
            "page_len": page_len,
            "bank_name": filters.get("bank_name"),
        },
    )

@frappe.whitelist()
def calculate_employee_loan_amount(loan_product , applicant , loan_eligibility_months):
    try:
        loan_product_doc = frappe.get_doc('Loan Product', loan_product)
        if not loan_product_doc:
            frappe.throw(f"Loan Product '{loan_product}' not found.")

        # Safely convert loan_eligibility_months to an integer
        try:
            loan_eligibility_months_int = int(loan_eligibility_months)
        except ValueError:
            frappe.throw(f"Invalid value for Loan Eligibility Months: '{loan_eligibility_months}'. Please provide a numeric value.")

        # Safely convert custom_loan_eligibility_months from the doc to an integer
        # Use .strip() to remove any leading/trailing whitespace before conversion
        allowed_eligibility_months_int = 0
        if loan_product_doc.custom_loan_eligibility_months:
            try:
                allowed_eligibility_months_int = int(str(loan_product_doc.custom_loan_eligibility_months).strip())
            except ValueError:
                frappe.throw(f"Invalid value for Custom Loan Eligibility Months in Loan Product: '{loan_product_doc.custom_loan_eligibility_months}'. Please ensure it's a numeric value.")


        if loan_eligibility_months_int > allowed_eligibility_months_int:
            frappe.throw(f"The Loan Eligibility Months value of {loan_eligibility_months_int} is greater than the allowed {allowed_eligibility_months_int}")

        loan_installment_deduction_percentage = loan_product_doc.custom_loan_installment_deduction_percentage

        salary_structure_assignment_list = frappe.get_all("Salary Structure" , filters={"payroll_frequency" : "Monthly"} , pluck='name')

        salary_structure_assignment_data = frappe.db.get_value(
            "Salary Structure Assignment",
            {
                "employee": applicant,
                "from_date": ("<=", today()),
                "docstatus": 1,
                "salary_structure": ["in" , salary_structure_assignment_list],
            },
            "*",
            order_by="from_date desc",
            as_dict=True,
        )

        if salary_structure_assignment_data:
            salary_structure_assignment_name = salary_structure_assignment_data.name

            basic_salary = float(frappe.db.get_value("Salary Structure Assignment", salary_structure_assignment_name, 'custom_basic_salary') or 0.0)
            calculated_loan_amount = basic_salary * loan_eligibility_months_int # Use the converted integer
            calculated_monthly_repayment_amount = basic_salary * loan_installment_deduction_percentage if loan_installment_deduction_percentage else 0

            return {
                "loan_amount": calculated_loan_amount,
                "monthly_repayment_amount": calculated_monthly_repayment_amount,
                "basic_salary": basic_salary
            }
        else:
            frappe.throw(f"No active Salary Structure Assignment found for Employee {applicant}")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in calculate_employee_loan_amount")
        frappe.throw(f"An error occurred during loan calculation: {str(e)}")

@frappe.whitelist()
def create_expense_claim_from_travel_request(travel_request_name):
    """
    Creates an Expense Claim from a submitted Travel Request.
    """
    if not travel_request_name:
        frappe.throw("Travel Request name is required.")

    travel_request_doc = frappe.get_doc("Travel Request", travel_request_name)

    if travel_request_doc.docstatus != 1:
        frappe.throw("Expense Claim can only be created from a submitted Travel Request.")

    # Create a new Expense Claim document
    expense_claim = frappe.new_doc("Expense Claim")

    # Set main fields
    expense_claim.employee = travel_request_doc.employee
    expense_claim.employee_name = travel_request_doc.employee_name
    expense_claim.posting_date = getdate() # Set current date for posting date
    expense_claim.department = frappe.db.get_value("Employee" , expense_claim.employee_name , 'Department')
    expense_claim.custom_travel_request = travel_request_doc.name
    
    # You might want to link the Expense Claim back to the Travel Request
    # Make sure 'travel_request' field exists in Expense Claim DocType or add it via Customize Form
    # expense_claim.travel_request = travel_request_doc.name


    # Add expenses from the 'expenses' child table of Travel Request
    if travel_request_doc.get("costings"): # Assuming the child table is named 'expenses'
        for expense_item in travel_request_doc.costings:
            expense_claim.append("expenses", { # Assuming 'expenses' is the child table in Expense Claim too
                "expense_date":  getdate(),
                "expense_type": expense_item.expense_type,
                "amount": expense_item.total_amount,
                "description": expense_item.comments,
                # Map other fields as needed from Travel Request's expense item to Expense Claim's expense item
                # Example:
                # "account": expense_item.account,
                # "cost_center": expense_item.cost_center,
            })
    else:
        frappe.msgprint("No expense items found in the Travel Request.")


    try:
        expense_claim.insert(ignore_mandatory=True, ignore_permissions=True) # Insert the new document
        # expense_claim.submit() # Optionally submit the expense claim automatically

        frappe.db.commit() # Commit the changes to the database

        return expense_claim.name # Return the name of the new document
    except Exception as e:
        frappe.db.rollback() # Rollback if any error occurs
        frappe.throw(f"Error creating Expense Claim: {frappe.utils.get_traceback()}")

@frappe.whitelist()
def calculate_employee_base(employee ):
    try:
        salary_structure_assignment_list = frappe.get_all("Salary Structure" , filters={"payroll_frequency" : "Monthly"} , pluck='name')

        salary_structure_assignment_data = frappe.db.get_value(
            "Salary Structure Assignment",
            {
                "employee": employee,
                "from_date": ("<=", today()),
                "docstatus": 1,
                "salary_structure": ["in" , salary_structure_assignment_list],
            },
            "*",
            order_by="from_date desc",
            as_dict=True,
        )

        if salary_structure_assignment_data:
            salary_structure_assignment_name = salary_structure_assignment_data.name

            basic_salary = float(frappe.db.get_value("Salary Structure Assignment", salary_structure_assignment_name, 'custom_basic_salary') or 0.0)
            
            return {
                "basic_salary": basic_salary
            }
        else:
            frappe.throw(f"No active Salary Structure Assignment found for Employee {applicant}")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in calculate_employee_loan_amount")
        frappe.throw(f"An error occurred during loan calculation: {str(e)}")



@frappe.whitelist()
# overried funcation on additional salaries to sum the amount of same components
def get_additional_salaries(employee, start_date, end_date, component_type):
    from frappe.query_builder import Criterion
    from frappe.query_builder.functions import Max, Min, Sum

    comp_type = "Earning" if component_type == "earnings" else "Deduction"

    additional_sal = frappe.qb.DocType("Additional Salary")
    component_field = additional_sal.salary_component.as_("component")
    overwrite_field = additional_sal.overwrite_salary_structure_amount.as_("overwrite")

    amount_sum = Sum(additional_sal.amount).as_("amount")
    additional_salary_list = (
        frappe.qb.from_(additional_sal)
        .select(
            additional_sal.name,
            component_field,
            additional_sal.type,
            amount_sum, 
            additional_sal.is_recurring,
            overwrite_field,
            additional_sal.deduct_full_tax_on_selected_payroll_date,
        )
        .groupby(
            component_field
            )
        .where(
            (additional_sal.employee == employee)
            & (additional_sal.docstatus == 1)
            & (additional_sal.type == comp_type)
            & (additional_sal.disabled == 0)
        )
        .where(
            Criterion.any(
                [
                    Criterion.all(
                        [  # is recurring and additional salary dates fall within the payroll period
                            additional_sal.is_recurring == 1,
                            additional_sal.from_date <= end_date,
                            additional_sal.to_date >= end_date,
                        ]
                    ),
                    Criterion.all(
                        [  # is not recurring and additional salary's payroll date falls within the payroll period
                            additional_sal.is_recurring == 0,
                            additional_sal.payroll_date[start_date:end_date],
                        ]
                    ),
                ]
            )
        )
        .run(as_dict=True)
    )


    additional_salaries = []
    components_to_overwrite = []

    for d in additional_salary_list:
        if d.overwrite:
            if d.component in components_to_overwrite:
                frappe.throw(
                    _(
                        "Multiple Additional Salaries with overwrite property exist for Salary Component {0} between {1} and {2}."
                    ).format(frappe.bold(d.component), start_date, end_date),
                    title=_("Error"),
                )

            components_to_overwrite.append(d.component)

        additional_salaries.append(d)

    return additional_salaries