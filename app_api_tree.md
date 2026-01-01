# API Tree

## hr_advance.api

- `fetch_bank_branch_list(doctype, txt, searchfield, start, page_len, filters)`
  - Link field query for bank branches

- `calculate_employee_loan_amount(loan_product, applicant, loan_eligibility_months)`
  - Calculate loan amount from basic salary
  - Returns: loan_amount, monthly_repayment_amount, basic_salary

- `create_expense_claim_from_travel_request(travel_request_name)`
  - Create Expense Claim from Travel Request
  - Returns: expense_claim.name

- `calculate_employee_base(employee)`
  - Get employee base salary from active Salary Structure Assignment
  - Returns: basic_salary

- `get_additional_salaries(employee, start_date, end_date, component_type)`
  - Get additional salaries with summed same components
  - Returns: List with summed amounts

## bulk_leave_allocation

- `get_active_employees(company, leave_type, from_date, to_date, department=None, yearly_leave_type=0)`
  - Get active employees with leave balances
  - Returns: List of employees with allocation details

- `create_bulk_leave_allocations(bulk_allocation_name)`
  - Create Leave Allocation documents for all employees
  - Returns: success_count, failed_count, failed list

## Scheduled Tasks

- `calculate_exp_yrears_in_employee()` - Daily: Calculate employee experience years
- `update_supplier_status()` - Daily: Update supplier status based on license expiry

## Document Events

- `summation_task_cost()` - Purchase Invoice on_submit
- `cancel_task_cost()` - Purchase Invoice on_cancel
- `validate_leave_no_earlier_submission_allowed()` - Leave Application validate
