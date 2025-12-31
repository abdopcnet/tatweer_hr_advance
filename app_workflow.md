# HR Advance - Workflow Diagrams

## Overview

Simple workflow documentation for hr_advance app processes.

## 1. Bulk Leave Allocation Workflow

```mermaid
flowchart TD
    A[User opens Leave Allocation List] --> B[Click Bulk Allocation Button]
    B --> C[Open Bulk Leave allocation Form]
    C --> D[Fill Company, Leave Type, Dates]
    D --> E[Click Get Active Employees]
    E --> F[Fetch Active Employees]
    F --> G[Calculate Unused Leaves]
    G --> H[Populate Child Table]
    H --> I[User Reviews/Edits Table]
    I --> J[Click Create Bulk Leave Allocations]
    J --> K[Validate Each Row]
    K --> L{Valid?}
    L -->|Yes| M[Create Leave Allocation]
    L -->|No| N[Log Error]
    M --> O[Submit Leave Allocation]
    O --> P[Return Success/Failed Count]
    N --> P
```

## 2. Earned Leaves Allocation Workflow (HRMS)

```mermaid
flowchart TD
    A[Scheduler Runs Daily] --> B[Call allocate_earned_leaves]
    B --> C[Get Earned Leave Types]
    C --> D[For Each Leave Type]
    D --> E[Get Active Leave Allocations]
    E --> F{Has Leave Policy?}
    F -->|No| G[Skip]
    F -->|Yes| H[Get annual_allocation from Leave Policy Detail]
    H --> I[Check Effective Date]
    I --> J{Is First Day of Month?}
    J -->|No| G
    J -->|Yes| K[Calculate earned_leaves = annual_allocation / 12]
    K --> L[Update total_leaves_allocated]
    L --> M[Create Leave Ledger Entry]
    M --> N[Add Comment to Allocation]
```

## 3. Leave Allocation Field Flow

```mermaid
flowchart LR
    A[Leave Policy Detail] -->|annual_allocation| B[30 days]
    B --> C[get_monthly_earned_leave]
    C --> D[earned_leaves = 30 / 12]
    D --> E[2.5 days]
    E --> F[Leave Allocation]
    F --> G[total_leaves_allocated]
    G --> H[unused_leaves + new_leaves_allocated]
```

## 4. Bulk Leave Allocation Data Flow

```mermaid
flowchart TD
    A[Bulk Leave allocation] --> B[company, leave_type, from_date, to_date]
    B --> C[get_active_employees API]
    C --> D[Filter Active Employees]
    D --> E[Get Carry Forwarded Leaves]
    E --> F[Bulk Leave allocation Table]
    F --> G[new_leaves_allocated]
    F --> H[carry_forward]
    F --> I[total_leaves_allocated]
    G --> J[create_bulk_leave_allocations API]
    H --> J
    I --> J
    J --> K[Create Leave Allocation]
    K --> L[set_total_leaves_allocated]
    L --> M[Submit Leave Allocation]
```

## 5. Scheduled Tasks Workflow

```mermaid
flowchart TD
    A[Scheduler Daily Event] --> B[calculate_exp_yrears_in_employee]
    A --> C[update_supplier_status]
    B --> D[Update Employee.custom_total_insed_experience_in_years]
    D --> E[Update Employee.custom_total_experience_in_years]
    C --> F[Get Suppliers with Expired License]
    F --> G{License Expired?}
    G -->|Yes| H[Set is_frozen = 1]
    G -->|No| I[Skip]
    H --> J[Add Comment to Supplier]
```

## 6. Yearly Leave Type Logic

```mermaid
flowchart TD
    A[Select Leave Type] --> B[Fetch custom_yearly_leave_type]
    B --> C{yearly_leave_type = 1?}
    C -->|Yes| D[Copy total_leaves_allocated to new_leaves_allocated]
    C -->|No| E[Clear new_leaves_allocated, Make Required]
    D --> F[Make new_leaves_allocated Non-Mandatory]
    E --> G[Make new_leaves_allocated Mandatory]
    F --> H[User Can Edit]
    G --> H
```
