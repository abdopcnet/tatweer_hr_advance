# File Structure

## Overview

Simple file structure tree for hr_advance app.

## Directory Structure

```
hr_advance/
├── hr_advance/
│   ├── __init__.py
│   ├── api.py                    # API methods
│   ├── event.py                  # Document event handlers
│   ├── hooks.py                  # App hooks and configuration
│   ├── tasks.py                  # Scheduled tasks
│   ├── modules.txt               # App modules
│   ├── patches.txt               # Database patches
│   ├── config/                   # Configuration files
│   ├── custom/                   # Custom DocType definitions
│   ├── hr_advance/               # Main module
│   │   ├── __init__.py
│   │   ├── doctype/              # DocType definitions
│   │   │   ├── bank_branch/
│   │   │   ├── bulk_leave_allocation/
│   │   │   ├── bulk_leave_allocation_table/
│   │   │   ├── course_classification/
│   │   │   ├── department_type/
│   │   │   ├── designation_type/
│   │   │   ├── employee_bank/
│   │   │   ├── employee_bank_branch/
│   │   │   ├── employee_training_request/
│   │   │   ├── exit_permission_request/
│   │   │   └── training_course_available/
│   │   └── report/               # Custom reports
│   ├── override/                 # Override core DocTypes
│   │   └── py/
│   │       ├── employee.py
│   │       ├── payroll_entry.py
│   │       └── salary_slip.py
│   └── public/                   # Public assets
│       └── js/                   # JavaScript files
│           ├── employee.js
│           ├── loan.js
│           ├── loan_application.js
│           ├── travel_request.js
│           └── additional_salary.js
├── license.txt
├── pyproject.toml
└── README.md
```

## Key Files

### Configuration

-   `hooks.py`: App hooks, doctype_js, doc_events, scheduler_events, override_doctype_class
-   `modules.txt`: App modules list
-   `patches.txt`: Database migration patches

### API and Logic

-   `api.py`: Whitelisted API methods
-   `event.py`: Document event handlers (on_submit, on_cancel, validate)
-   `tasks.py`: Scheduled tasks (daily, hourly, etc.)

### DocType Structure

Each DocType has:

-   `{doctype_name}.json`: DocType definition
-   `{doctype_name}.py`: Python controller
-   `{doctype_name}.js`: Client-side JavaScript
-   `__init__.py`: Package initialization

### Overrides

-   `override/py/`: Python class overrides for core DocTypes
-   `override/js/`: JavaScript overrides (if any)

## DocType Pattern

```
doctype/
└── {doctype_name}/
    ├── __init__.py
    ├── {doctype_name}.json      # DocType definition
    ├── {doctype_name}.py         # Server-side logic
    ├── {doctype_name}.js         # Client-side logic
    └── {doctype_name}_list.js    # List view customization (optional)
```

## Important Notes

-   All DocTypes are in `hr_advance/hr_advance/doctype/`
-   Custom fields are stored in `custom/` directory
-   Reports are in `hr_advance/hr_advance/report/`
-   Public assets (JS/CSS) are in `public/`
-   Overrides extend core ERPNext/HRMS functionality
