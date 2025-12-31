# API Tree

## Overview

Simple API structure listing all whitelisted methods in hr_advance app.

## API Methods

### hr_advance.api

-   `fetch_bank_branch_list(doctype, txt, searchfield, start, page_len, filters)`

    -   Description: Fetch bank branch list for employee bank field
    -   Parameters: doctype, txt (search text), searchfield, start (offset), page_len (limit), filters (dict with bank_name)

-   `calculate_employee_loan_amount(loan_product, applicant, loan_eligibility_months)`

    -   Description: Calculate loan amount based on basic salary and eligibility months
    -   Parameters: loan_product, applicant (employee), loan_eligibility_months
    -   Returns: loan_amount, monthly_repayment_amount, basic_salary

-   `create_expense_claim_from_travel_request(travel_request_name)`

    -   Description: Creates Expense Claim from submitted Travel Request
    -   Parameters: travel_request_name
    -   Returns: expense_claim.name

-   `calculate_employee_base(employee)`

    -   Description: Calculate employee base salary from active Salary Structure Assignment
    -   Parameters: employee
    -   Returns: basic_salary

-   `get_additional_salaries(employee, start_date, end_date, component_type)`
    -   Description: Get additional salaries with summed amounts for same components
    -   Parameters: employee, start_date, end_date, component_type (earnings/deductions)
    -   Returns: List of additional salaries with summed amounts

### hr_advance.hr_advance.doctype.bulk_leave_allocation.bulk_leave_allocation

-   `get_active_employees(company, leave_type, from_date, to_date, department=None, yearly_leave_type=0)`

    -   Description: Get active employees with their leave balances for bulk allocation
    -   Parameters: company, leave_type, from_date, to_date, department (optional), yearly_leave_type (0 or 1)
    -   Returns: List of employees with leave balances and allocation details

-   `create_bulk_leave_allocations(bulk_allocation_name)`
    -   Description: Create Leave Allocation documents in background for all employees
    -   Parameters: bulk_allocation_name
    -   Returns: success_count, failed_count, failed (list of failed allocations)

### hr_advance.hr_advance.tasks

-   `calculate_exp_yrears_in_employee()`

    -   Description: Calculate total experience years for active employees (scheduled task)
    -   Parameters: None
    -   Updates: custom_total_insed_experience_in_years, custom_total_experience_in_years

-   `update_supplier_status()`
    -   Description: Update supplier status based on license expiration date (scheduled task)
    -   Parameters: None
    -   Updates: is_frozen field for expired suppliers

### hr_advance.hr_advance.event

-   `summation_task_cost(doc, method)`

    -   Description: Sum task costs from Purchase Invoices on submit
    -   Parameters: doc (Purchase Invoice), method
    -   Event: Purchase Invoice on_submit

-   `cancel_task_cost(doc, method)`

    -   Description: Recalculate task costs on Purchase Invoice cancel
    -   Parameters: doc (Purchase Invoice), method
    -   Event: Purchase Invoice on_cancel

-   `validate_leave_no_earlier_submission_allowed(doc, method)`
    -   Description: Validate leave application dates (no future dates allowed)
    -   Parameters: doc (Leave Application), method
    -   Event: Leave Application validate

### hr_advance.hr_advance.override.py.payroll_entry

-   `overrid_payroll_entry` (class methods)
    -   Description: Override Payroll Entry processing
    -   Methods: Multiple whitelisted methods for payroll processing

## Usage

All methods are whitelisted and can be called from client-side using `frappe.call()`:

```javascript
frappe.call({
	method: 'hr_advance.api.calculate_employee_loan_amount',
	args: {
		loan_product: 'LOAN-001',
		applicant: 'EMP-001',
		loan_eligibility_months: 12,
	},
	callback: function (r) {
		// Handle response
	},
});
```
