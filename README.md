# Hr Advance

![Version](https://img.shields.io/badge/version-31.12.2025-blue)

Advanced HR management features in compliance with Libyan labor regulations.

## Features Preview

### Payroll & Salary Management

-   **Salary Slip Override**: Enhanced salary slip processing with custom additional salary components
-   **Payroll Entry Override**: Custom bank entry and journal entry processing for payroll
-   **Designation Type**: Custom DocType for managing designation types with salary details (basic salary, responsibility bonus, allowances)
-   **Additional Salary**: Summed calculation of same components for accurate payroll processing

### Employee Management

-   **Employee Override**: Custom employee naming and approvers section
-   **Experience Calculation**: Daily scheduled task to calculate employee experience years
-   **Bank Branch Management**: Custom DocTypes for employee bank and bank branch management
-   **Employee Training**: Training request management with course classification

### Loans & Advances

-   **Loan Calculation**: API method to calculate loan amounts based on basic salary and eligibility months
-   **Loan Application**: Enhanced loan application processing with custom JavaScript
-   **Employee Advance**: Bank-only mode of payment filter

### Leave & Attendance

-   **Bulk Leave Allocation**: Create leave allocations for multiple employees at once with automatic carry forward calculation
-   **Leave Validation**: Prevents submission of leave applications with earlier dates
-   **Attendance Report**: Custom attendance reporting with late entry and early exit tracking
-   **Exit Permission**: Exit permission request DocType and reporting

### Travel & Expenses

-   **Travel Request**: Enhanced travel request processing with expense claim integration
-   **Expense Claim Creation**: Automatic expense claim creation from travel requests

### Integration & Automation

-   **Purchase Invoice Integration**: Automatic task cost summation on invoice submission
-   **Supplier Status Update**: Daily scheduled task to update supplier status
-   **Additional Salaries API**: Override function to sum amounts of same salary components

### Reports

-   **Attendance Report**: Detailed attendance tracking with in/out time, late entries, early exits
-   **Exit Permission Report**: Exit permission request reporting and analytics

## Earned Leaves Workflow (HRMS Integration)

### Overview

Earned Leaves are automatically allocated to employees based on Leave Policy configuration. The system uses a scheduled task that runs daily to allocate leaves.

### Step-by-Step Process

1. **Leave Type Configuration** (`tabLeave Type`)

    - Set `is_earned_leave = 1`
    - Set `earned_leave_frequency = "Monthly"` (or Quarterly, Half-Yearly, Yearly)
    - Set `allocate_on_day = "First Day"` (or "Last Day", "Date of Joining")

2. **Leave Policy Setup** (`tabLeave Policy`)

    - Create Leave Policy with `leave_policy_details` child table
    - In `tabLeave Policy Detail`, set `annual_allocation` field (e.g., 30 days)

3. **Leave Policy Assignment** (`tabLeave Policy Assignment`)

    - Assign Leave Policy to Employee
    - System creates initial `tabLeave Allocation` with `from_date` and `to_date`

4. **Scheduled Task Execution** (`hrms.hr.utils.allocate_earned_leaves`)

    - Runs daily via `daily_long` scheduler event
    - Checks if today matches `allocate_on_day` for each Earned Leave Type
    - For Monthly frequency with First Day: checks if today is first day of month

5. **Leave Calculation**

    - Fetches `annual_allocation` from `tabLeave Policy Detail`
    - Calculates `earned_leaves = annual_allocation / 12` (for Monthly)
    - Example: 30 days / 12 = 2.5 days per month

6. **Allocation Update**
    - Updates `tabLeave Allocation.total_leaves_allocated` field
    - Formula: `total_leaves_allocated = existing_total + earned_leaves`
    - Creates `tabLeave Ledger Entry` with transaction_type = "Leave Allocation"
    - Adds comment to Leave Allocation document

### Field Locations

-   **annual_allocation**: `tabLeave Policy Detail.annual_allocation` (Float)
-   **earned_leaves**: Calculated dynamically, not stored
-   **total_leaves_allocated**: `tabLeave Allocation.total_leaves_allocated` (Float)
-   **unused_leaves**: `tabLeave Allocation.unused_leaves` (Float, carry forward balance)
-   **new_leaves_allocated**: `tabLeave Allocation.new_leaves_allocated` (Float)

### Key Functions

-   `allocate_earned_leaves()`: Main scheduler function in `hrms/hr/utils.py`
-   `get_monthly_earned_leave()`: Calculates earned leaves based on frequency
-   `check_effective_date()`: Validates if allocation should run today
-   `update_previous_leave_allocation()`: Updates existing allocation with new leaves

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench --site [site_name] install-app hr_advance
```

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/hr_advance
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

-   ruff
-   eslint
-   prettier
-   pyupgrade

## License

MIT
