# HR Advance - File Structure

## Overview

Simple file structure documentation for hr_advance app.

## Directory Tree

```
hr_advance/
├── hr_advance/
│   ├── __init__.py
│   ├── api.py                    # API methods
│   ├── event.py                  # Document event handlers
│   ├── hooks.py                  # App hooks configuration
│   ├── tasks.py                  # Scheduled tasks
│   ├── modules.txt               # Module definition
│   ├── patches.txt               # Migration patches
│   ├── config/                   # Configuration files
│   ├── override/                 # Core DocType overrides
│   │   └── py/
│   │       ├── employee.py
│   │       ├── payroll_entry.py
│   │       └── salary_slip.py
│   ├── public/                   # Client-side assets
│   │   └── js/
│   │       ├── employee.js
│   │       ├── loan.js
│   │       ├── loan_application.js
│   │       ├── travel_request.js
│   │       └── additional_salary.js
│   ├── templates/                # Jinja templates
│   │   └── pages/
│   └── hr_advance/               # Main module
│       ├── __init__.py
│       ├── custom/               # Custom fields
│       │   └── leave_type.json
│       ├── doctype/              # Custom DocTypes
│       │   ├── bank_branch/
│       │   ├── bulk_leave_allocation/
│       │   ├── bulk_leave_allocation_table/
│       │   ├── course_classification/
│       │   ├── department_type/
│       │   ├── designation_type/
│       │   ├── employee_bank/
│       │   ├── employee_bank_branch/
│       │   ├── employee_training_request/
│       │   ├── exit_permission_request/
│       │   └── training_course_available/
│       └── report/               # Custom reports
│           ├── attendance_report/
│           └── exit_permission_report/
├── README.md
├── license.txt
└── pyproject.toml
```

## DocTypes

### Leave Management

-   **Bulk Leave allocation**: Bulk leave allocation for multiple employees
-   **Bulk Leave allocation Table**: Child table for employee leave details

### Employee Management

-   **Designation Type**: Designation types with salary details
-   **Department Type**: Department type classification
-   **Employee Bank**: Employee bank account information
-   **Employee Bank Branch**: Bank branch details for employees
-   **Employee Training Request**: Training request management
-   **Training Course Available**: Available training courses
-   **Course Classification**: Course classification system
-   **Exit Permission Request**: Exit permission management

### Banking

-   **Bank Branch**: Bank branch master data

## Reports

-   **Attendance Report**: Detailed attendance tracking with late/early entries
-   **Exit Permission Report**: Exit permission analytics

## Overrides

### Core DocType Overrides

-   **Employee**: Custom employee naming and approvers
-   **Salary Slip**: Enhanced salary slip processing
-   **Payroll Entry**: Custom bank entry and journal entry processing

## Custom Fields

-   **Leave Type**: `custom_no_earlier_submission_allowed` (Check)
-   **Leave Type**: `custom_yearly_leave_type` (Check)

## Scheduled Tasks

### Daily Tasks

-   `calculate_exp_yrears_in_employee`: Calculate employee experience years
-   `update_supplier_status`: Update supplier status based on license expiration

## Client Scripts

-   `employee.js`: Employee form customizations
-   `loan.js`: Loan form customizations
-   `loan_application.js`: Loan application form customizations
-   `travel_request.js`: Travel request form customizations
-   `additional_salary.js`: Additional salary form customizations
