# Hr Advance

![Version](https://img.shields.io/badge/version-31.12.2025-blue)

Advanced HR management features in compliance with Libyan labor regulations.

## Features Preview

### Payroll & Salary Management
- **Salary Slip Override**: Enhanced salary slip processing with custom additional salary components
- **Payroll Entry Override**: Custom bank entry and journal entry processing for payroll
- **Designation Type**: Custom DocType for managing designation types with salary details (basic salary, responsibility bonus, allowances)
- **Additional Salary**: Summed calculation of same components for accurate payroll processing

### Employee Management
- **Employee Override**: Custom employee naming and approvers section
- **Experience Calculation**: Daily scheduled task to calculate employee experience years
- **Bank Branch Management**: Custom DocTypes for employee bank and bank branch management
- **Employee Training**: Training request management with course classification

### Loans & Advances
- **Loan Calculation**: API method to calculate loan amounts based on basic salary and eligibility months
- **Loan Application**: Enhanced loan application processing with custom JavaScript
- **Employee Advance**: Bank-only mode of payment filter

### Leave & Attendance
- **Leave Validation**: Prevents submission of leave applications with earlier dates
- **Attendance Report**: Custom attendance reporting with late entry and early exit tracking
- **Exit Permission**: Exit permission request DocType and reporting

### Travel & Expenses
- **Travel Request**: Enhanced travel request processing with expense claim integration
- **Expense Claim Creation**: Automatic expense claim creation from travel requests

### Integration & Automation
- **Purchase Invoice Integration**: Automatic task cost summation on invoice submission
- **Supplier Status Update**: Daily scheduled task to update supplier status
- **Additional Salaries API**: Override function to sum amounts of same salary components

### Reports
- **Attendance Report**: Detailed attendance tracking with in/out time, late entries, early exits
- **Exit Permission Report**: Exit permission request reporting and analytics

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

- ruff
- eslint
- prettier
- pyupgrade

## License

MIT
