# Leave Allocation Guide

## Overview

Step-by-step guide to create and manage Leave Allocations for employees.

## Steps

### 1. Automatic Allocation (Recommended)

**Via Leave Policy Assignment**

**Process:**

1. Create Leave Policy Assignment
2. Submit document
3. System automatically creates Leave Allocation documents
4. No manual intervention needed

**Location:** HR → Leave Policy Assignment → New

---

### 2. Manual Allocation

**DocType:** `Leave Allocation`

**Required Fields:**

-   `employee` (Link): Employee name
-   `leave_type` (Link): Leave Type name
-   `from_date` (Date): Allocation start date
-   `to_date` (Date): Allocation end date
-   `new_leaves_allocated` (Float): Number of new days to allocate
-   `total_leaves_allocated` (Float): Total leaves (auto-calculated)

**Optional Fields:**

-   `carry_forward` (Check): Enable carry forward from previous allocation
-   `unused_leaves` (Float): Carry forward balance (auto-calculated)
-   `leave_policy` (Link): Link to Leave Policy
-   `leave_policy_assignment` (Link): Link to Leave Policy Assignment

**Process:**

1. Select employee and leave_type
2. Set from_date and to_date
3. Enter new_leaves_allocated
4. Enable carry_forward if needed
5. System calculates total_leaves_allocated
6. Submit document

**Location:** HR → Leave Allocation → New

---

### 3. Bulk Allocation (hr_advance)

**DocType:** `Bulk Leave allocation`

**Required Fields:**

-   `company` (Link): Company name
-   `leave_type` (Link): Leave Type name
-   `from_date` (Date): Allocation start date
-   `to_date` (Date): Allocation end date

**Process:**

1. Fill company, leave_type, from_date, to_date
2. Click "Get Active Employees" button
3. System populates child table with employees
4. Review/edit new_leaves_allocated in table
5. Click "Create Bulk Leave Allocations" button
6. System creates Leave Allocation for each employee

**Location:** HR → Bulk Leave allocation → New

---

## Field Reference

### Leave Allocation Fields

-   `tabLeave Allocation.employee`: Employee link
-   `tabLeave Allocation.leave_type`: Leave Type name
-   `tabLeave Allocation.from_date`: Allocation start date
-   `tabLeave Allocation.to_date`: Allocation end date
-   `tabLeave Allocation.new_leaves_allocated`: New days allocated
-   `tabLeave Allocation.carry_forward`: Carry forward flag
-   `tabLeave Allocation.unused_leaves`: Carry forward balance
-   `tabLeave Allocation.total_leaves_allocated`: Total leaves (unused + new)
-   `tabLeave Allocation.leave_policy`: Leave Policy link
-   `tabLeave Allocation.leave_policy_assignment`: Assignment link

### Calculation

```
total_leaves_allocated = unused_leaves + new_leaves_allocated
```

---

## Earned Leaves Allocation

### Automatic Monthly Allocation

**Scheduler:** `hrms.hr.utils.allocate_earned_leaves` (runs daily)

**Requirements:**

-   Leave Type: `is_earned_leave = 1`
-   Leave Type: `earned_leave_frequency = "Monthly"`
-   Leave Type: `allocate_on_day = "First Day"`
-   Leave Allocation: Must have `leave_policy_assignment` or `leave_policy`

**Process:**

1. Scheduler checks if today matches allocate_on_day
2. Fetches annual_allocation from Leave Policy Detail
3. Calculates: `earned_leaves = annual_allocation / 12`
4. Updates `total_leaves_allocated` in Leave Allocation
5. Creates Leave Ledger Entry
6. Adds comment to Leave Allocation

**Example:**

-   annual_allocation = 30 days
-   earned_leaves = 30 / 12 = 2.5 days per month
-   Added on first day of each month

---

## Carry Forward

### Enable Carry Forward

**In Leave Allocation:**

-   Set `carry_forward = 1`
-   System calculates `unused_leaves` from previous allocation
-   Adds to `total_leaves_allocated`

**In Leave Policy Assignment:**

-   Set `carry_forward = 1`
-   Applied to all Leave Allocations created from assignment

**Calculation:**

-   `unused_leaves` = Remaining balance from previous allocation period
-   `total_leaves_allocated` = `unused_leaves` + `new_leaves_allocated`

---

## Quick Setup Checklist

-   [ ] Create Leave Policy with leave types and annual_allocation
-   [ ] Assign Leave Policy to employee (creates allocations automatically)
-   [ ] OR create Leave Allocation manually
-   [ ] OR use Bulk Leave allocation for multiple employees
-   [ ] Verify total_leaves_allocated is correct
-   [ ] Enable carry_forward if needed
-   [ ] Submit Leave Allocation
-   [ ] Check Leave Ledger Entry created

---

## Notes

-   Leave Allocation must be submitted to be effective
-   total_leaves_allocated is auto-calculated on save
-   unused_leaves is calculated from previous allocation if carry_forward enabled
-   For earned leaves, ensure Leave Allocation has leave_policy_assignment link
-   Scheduler automatically adds earned leaves on allocate_on_day
-   Overlapping allocations are not allowed for same employee and leave_type
