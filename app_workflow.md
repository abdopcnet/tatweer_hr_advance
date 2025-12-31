# Workflow

## Overview

Simple workflow diagrams for hr_advance app processes.

## Main Workflows

### Employee Onboarding

```mermaid
flowchart TD
    A[Create Employee] --> B[Assign Leave Policy]
    B --> C[Assign Salary Structure]
    C --> D[Employee Onboarding]
    D --> E[Complete Activities]
    E --> F[Employee Active]
```

### Leave Management

```mermaid
flowchart TD
    A[Create Leave Type] --> B[Create Leave Policy]
    B --> C[Assign Leave Policy to Employee]
    C --> D[Leave Allocation Created]
    D --> E[Employee Applies for Leave]
    E --> F[Leave Approver Reviews]
    F --> G{Approved?}
    G -->|Yes| H[Leave Approved]
    G -->|No| I[Leave Rejected]
    H --> J[Leave Ledger Updated]
```

### Bulk Leave Allocation

```mermaid
flowchart TD
    A[Create Bulk Leave Allocation] --> B[Select Company/Leave Type/Dates]
    B --> C[Click Get Active Employees]
    C --> D[Child Table Populated]
    D --> E[Review/Edit Allocations]
    E --> F[Click Create Bulk Leave Allocations]
    F --> G[Leave Allocations Created]
    G --> H[Allocations Submitted]
```

### Payroll Processing

```mermaid
flowchart TD
    A[Create Salary Structure] --> B[Assign to Employee]
    B --> C[Create Payroll Entry]
    C --> D[Select Employees]
    D --> E[Calculate Salaries]
    E --> F[Create Salary Slips]
    F --> G[Submit Payroll Entry]
    G --> H[Bank Entry Created]
    H --> I[Journal Entry Created]
```

### Training Management

```mermaid
flowchart TD
    A[Create Course Classification] --> B[Create Training Course]
    B --> C[Employee Training Request]
    C --> D[Manager Comments]
    D --> E[HR Comments]
    E --> F{Approved?}
    F -->|Yes| G[Training Scheduled]
    F -->|No| H[Request Rejected]
```

### Exit Permission

```mermaid
flowchart TD
    A[Employee Creates Exit Permission Request] --> B[Fill Date/Time/Reason]
    B --> C[Submit Request]
    C --> D[Leave Approver Reviews]
    D --> E{Approved?}
    E -->|Yes| F[Permission Granted]
    E -->|No| G[Permission Rejected]
```

## DocType Relationships

### Leave Management

-   Leave Type → Leave Policy → Leave Policy Assignment → Leave Allocation → Leave Application

### Payroll

-   Salary Component → Salary Structure → Salary Structure Assignment → Payroll Entry → Salary Slip

### Employee Management

-   Employee → Leave Policy Assignment → Leave Allocation
-   Employee → Salary Structure Assignment → Payroll Entry
-   Employee → Employee Onboarding → Employee Active

## Key Processes

1. **Leave Allocation**: Automatic via Leave Policy Assignment or Manual via Bulk Leave Allocation
2. **Payroll**: Monthly/Weekly processing via Payroll Entry
3. **Training**: Request-based workflow with approvals
4. **Exit Permission**: Time-based permission requests
