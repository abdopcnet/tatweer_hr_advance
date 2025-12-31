# HR Advance - API Structure

## Overview

Simple API structure documentation for hr_advance app whitelisted methods.

## API Methods

### 1. Bulk Leave Allocation APIs

#### `get_active_employees`

**Location:** `hr_advance.hr_advance.doctype.bulk_leave_allocation.bulk_leave_allocation.get_active_employees`

**Parameters:**

-   `company` (str): Company name
-   `leave_type` (str): Leave Type name
-   `from_date` (str): Allocation start date
-   `to_date` (str): Allocation end date
-   `department` (str, optional): Department filter

**Returns:**

```python
[
    {
        "employee": str,
        "employee_name": str,
        "department": str,
        "company": str,
        "leave_type": str,
        "from_date": str,
        "to_date": str,
        "new_leaves_allocated": float,
        "carry_forward": int,
        "total_leaves_allocated": float
    }
]
```

#### `create_bulk_leave_allocations`

**Location:** `hr_advance.hr_advance.doctype.bulk_leave_allocation.bulk_leave_allocation.create_bulk_leave_allocations`

**Parameters:**

-   `bulk_allocation_name` (str): Bulk Leave allocation document name

**Returns:**

```python
{
    "success_count": int,
    "failed_count": int,
    "failed": [
        {
            "employee": str,
            "employee_name": str,
            "error": str
        }
    ]
}
```

### 2. Employee & Loan APIs

#### `fetch_bank_branch_list`

**Location:** `hr_advance.api.fetch_bank_branch_list`

**Parameters:**

-   `doctype` (str): DocType name
-   `txt` (str): Search text
-   `searchfield` (str): Field to search
-   `start` (int): Pagination start
-   `page_len` (int): Page length
-   `filters` (dict): Filters dict with `bank_name`

**Returns:** SQL result list

#### `calculate_employee_loan_amount`

**Location:** `hr_advance.api.calculate_employee_loan_amount`

**Parameters:**

-   `loan_product` (str): Loan Product name
-   `applicant` (str): Employee name
-   `loan_eligibility_months` (int): Eligibility months

**Returns:**

```python
{
    "loan_amount": float,
    "monthly_repayment_amount": float,
    "basic_salary": float
}
```

#### `calculate_employee_base`

**Location:** `hr_advance.api.calculate_employee_base`

**Parameters:**

-   `employee` (str): Employee name

**Returns:**

```python
{
    "basic_salary": float
}
```

### 3. Travel & Expense APIs

#### `create_expense_claim_from_travel_request`

**Location:** `hr_advance.api.create_expense_claim_from_travel_request`

**Parameters:**

-   `travel_request_name` (str): Travel Request document name

**Returns:** Expense Claim document name (str)

### 4. Payroll APIs

#### `get_additional_salaries`

**Location:** `hr_advance.api.get_additional_salaries`

**Parameters:**

-   `employee` (str): Employee name
-   `start_date` (str): Period start date
-   `end_date` (str): Period end date
-   `component_type` (str): "earnings" or "deductions"

**Returns:**

```python
[
    {
        "name": str,
        "component": str,
        "type": str,
        "amount": float,
        "is_recurring": int,
        "overwrite": int,
        "deduct_full_tax_on_selected_payroll_date": int
    }
]
```

### 5. Scheduled Task APIs

#### `calculate_exp_yrears_in_employee`

**Location:** `hr_advance.tasks.calculate_exp_yrears_in_employee`

**Parameters:** None

**Returns:** None (updates Employee records)

#### `update_supplier_status`

**Location:** `hr_advance.tasks.update_supplier_status`

**Parameters:** None

**Returns:** None (updates Supplier records)

## Event Handlers

### Document Events

#### `summation_task_cost`

**Location:** `hr_advance.event.summation_task_cost`

**Trigger:** Purchase Invoice `on_submit`

**Parameters:**

-   `doc`: Purchase Invoice document
-   `method`: Event method name

#### `cancel_task_cost`

**Location:** `hr_advance.event.cancel_task_cost`

**Trigger:** Purchase Invoice `on_cancel`

**Parameters:**

-   `doc`: Purchase Invoice document
-   `method`: Event method name

#### `validate_leave_no_earlier_submission_allowed`

**Location:** `hr_advance.event.validate_leave_no_earlier_submission_allowed`

**Trigger:** Leave Application `validate`

**Parameters:**

-   `doc`: Leave Application document
-   `method`: Event method name
