# Earned Leaves Setup Guide

## Overview

Step-by-step guide to setup automatic monthly leave allocation (Earned Leaves) for employees.

## What are Earned Leaves?

Earned Leaves are automatically allocated to employees based on Leave Policy configuration. The system uses a scheduled task that runs daily to allocate leaves monthly, quarterly, half-yearly, or yearly.

**Example:** 30 days annual allocation = 2.5 days per month (30 / 12)

---

## Prerequisites

### 1. Leave Type Configuration

**DocType:** `Leave Type`

**Required Settings:**

-   `is_earned_leave` (Check) = **1** (Enable Earned Leave)
-   `earned_leave_frequency` (Select) = **"Monthly"** (or Quarterly, Half-Yearly, Yearly)
-   `allocate_on_day` (Select) = **"First Day"** (or "Last Day", "Date of Joining")

**Optional Settings:**

-   `rounding` (Select): 0.25, 0.5, 1.0 (for rounding earned leaves)
-   `is_carry_forward` (Check): Enable carry forward of unused leaves
-   `max_leaves_allowed` (Float): Maximum leaves allowed per period

**Location:** HR → Leave Type → [Select Leave Type] → Edit

**Example:**

```
Leave Type: "Annual Leave"
- is_earned_leave = 1
- earned_leave_frequency = "Monthly"
- allocate_on_day = "First Day"
- rounding = 0.5
```

---

### 2. Create Leave Policy

**DocType:** `Leave Policy`

**Required Fields:**

-   `title` (Data): Policy name (e.g., "Standard Leave Policy")

**Child Table:** `leave_policy_details` (Leave Policy Detail)

**Required Fields (per row):**

-   `leave_type` (Link): Select Earned Leave Type
-   `annual_allocation` (Float): Total days per year (e.g., 30)

**Process:**

1. Create Leave Policy with title
2. Add row in `leave_policy_details` table
3. Select `leave_type` (must be Earned Leave Type)
4. Enter `annual_allocation` (e.g., 30 days)
5. Submit Leave Policy

**Location:** HR → Leave Policy → New

**Example:**

```
Leave Policy: "Standard Leave Policy"
- leave_policy_details:
  - leave_type: "Annual Leave"
  - annual_allocation: 30
```

---

### 3. Assign Policy to Employee

**DocType:** `Leave Policy Assignment`

**Required Fields:**

-   `employee` (Link): Employee name
-   `leave_policy` (Link): Leave Policy to assign
-   `effective_from` (Date): Policy start date
-   `effective_to` (Date): Policy end date

**Optional Fields:**

-   `assignment_based_on` (Select): "Leave Period" or "Joining Date"
-   `leave_period` (Link): Required if assignment_based_on = "Leave Period"
-   `carry_forward` (Check): Enable carry forward of unused leaves

**Process:**

1. Select employee
2. Select leave_policy
3. Set effective_from (usually date_of_joining)
4. Set effective_to (usually end of year)
5. Enable carry_forward if needed
6. Submit document
7. System automatically creates Leave Allocation documents

**Location:** HR → Leave Policy Assignment → New

**Important:** Leave Allocation must have `leave_policy_assignment` or `leave_policy` link for scheduler to work.

---

## How Automatic Allocation Works

### Scheduler Process

**Function:** `hrms.hr.utils.allocate_earned_leaves`

**Schedule:** Runs daily via `daily_long` scheduler event

**Process:**

1. Gets all Leave Types where `is_earned_leave = 1`
2. Gets active Leave Allocations for each Earned Leave Type
3. Checks if Leave Allocation has `leave_policy_assignment` or `leave_policy`
4. If today matches `allocate_on_day`:
    - Fetches `annual_allocation` from Leave Policy Detail
    - Calculates: `earned_leaves = annual_allocation / 12` (for Monthly)
    - Updates `total_leaves_allocated` in Leave Allocation
    - Creates Leave Ledger Entry
    - Adds comment to Leave Allocation

### Calculation Formula

**For Monthly Frequency:**

```
earned_leaves = annual_allocation / 12
```

**Example:**

-   `annual_allocation` = 30 days
-   `earned_leaves` = 30 / 12 = 2.5 days per month

**For Other Frequencies:**

-   Quarterly: `annual_allocation / 4`
-   Half-Yearly: `annual_allocation / 2`
-   Yearly: `annual_allocation / 1`

---

## Allocation Day Options

### First Day of Month

**Setting:** `allocate_on_day = "First Day"`

**Behavior:**

-   Allocates leaves on the first day of each month
-   Example: January 1, February 1, March 1, etc.

### Last Day of Month

**Setting:** `allocate_on_day = "Last Day"`

**Behavior:**

-   Allocates leaves on the last day of each month
-   Example: January 31, February 28/29, March 31, etc.

### Date of Joining

**Setting:** `allocate_on_day = "Date of Joining"`

**Behavior:**

-   Allocates leaves on the same day of each month as date_of_joining
-   Example: If employee joined on 15th, allocates on 15th of each month

---

## Field Reference

### Leave Type Fields

-   `tabLeave Type.is_earned_leave`: Enable Earned Leave (Check)
-   `tabLeave Type.earned_leave_frequency`: Frequency (Monthly/Quarterly/Half-Yearly/Yearly)
-   `tabLeave Type.allocate_on_day`: Allocation day (First Day/Last Day/Date of Joining)
-   `tabLeave Type.rounding`: Rounding method (0.25/0.5/1.0)

### Leave Policy Fields

-   `tabLeave Policy.title`: Policy name
-   `tabLeave Policy.leave_policy_details`: Child table with leave types

### Leave Policy Detail Fields (Child Table)

-   `tabLeave Policy Detail.leave_type`: Leave Type link
-   `tabLeave Policy Detail.annual_allocation`: Days allocated per year

### Leave Policy Assignment Fields

-   `tabLeave Policy Assignment.employee`: Employee link
-   `tabLeave Policy Assignment.leave_policy`: Policy to assign
-   `tabLeave Policy Assignment.effective_from`: Start date
-   `tabLeave Policy Assignment.effective_to`: End date
-   `tabLeave Policy Assignment.carry_forward`: Carry forward flag

### Leave Allocation Fields

-   `tabLeave Allocation.employee`: Employee link
-   `tabLeave Allocation.leave_type`: Leave Type name
-   `tabLeave Allocation.leave_policy`: Leave Policy link (auto-filled)
-   `tabLeave Allocation.leave_policy_assignment`: Assignment link (auto-filled)
-   `tabLeave Allocation.total_leaves_allocated`: Total leaves (auto-updated)
-   `tabLeave Allocation.from_date`: Allocation start date
-   `tabLeave Allocation.to_date`: Allocation end date

---

## Quick Setup Checklist

-   [ ] Configure Leave Type:
    -   [ ] Set `is_earned_leave = 1`
    -   [ ] Set `earned_leave_frequency = "Monthly"`
    -   [ ] Set `allocate_on_day = "First Day"` (or "Last Day")
    -   [ ] Set `rounding` if needed
-   [ ] Create Leave Policy:
    -   [ ] Add title
    -   [ ] Add leave type to `leave_policy_details` table
    -   [ ] Set `annual_allocation` (e.g., 30 days)
    -   [ ] Submit Leave Policy
-   [ ] Assign Policy to Employee:
    -   [ ] Create Leave Policy Assignment
    -   [ ] Select employee and leave_policy
    -   [ ] Set effective_from and effective_to dates
    -   [ ] Submit document
    -   [ ] Verify Leave Allocation created automatically
-   [ ] Verify Scheduler:
    -   [ ] Check scheduler is running: `bench status`
    -   [ ] Wait for allocate_on_day (First Day or Last Day)
    -   [ ] Check Leave Allocation for updated `total_leaves_allocated`
    -   [ ] Check Leave Ledger Entry created
    -   [ ] Check comment added to Leave Allocation

---

## Troubleshooting

### Leaves Not Allocating Automatically

**Check 1: Leave Type Settings**

-   Verify `is_earned_leave = 1`
-   Verify `earned_leave_frequency` is set
-   Verify `allocate_on_day` is set

**Check 2: Leave Allocation Link**

-   Verify Leave Allocation has `leave_policy_assignment` or `leave_policy`
-   If NULL, scheduler will skip this allocation

**Check 3: Scheduler Status**

-   Run: `bench status`
-   Verify scheduler is running
-   Check logs: `logs/web.log` or `logs/worker.log`

**Check 4: Date Matching**

-   Verify today matches `allocate_on_day`
-   For "First Day": Check if today is first day of month
-   For "Last Day": Check if today is last day of month

**Check 5: Leave Policy Detail**

-   Verify `annual_allocation` exists in Leave Policy Detail
-   Verify `leave_type` matches in Leave Policy Detail

---

## Example: Complete Setup

### Step 1: Configure Leave Type

```
Leave Type: "Annual Leave"
- is_earned_leave: ✓ (checked)
- earned_leave_frequency: Monthly
- allocate_on_day: First Day
- rounding: 0.5
```

### Step 2: Create Leave Policy

```
Leave Policy: "Standard Policy"
- leave_policy_details:
  - leave_type: "Annual Leave"
  - annual_allocation: 30
```

### Step 3: Assign to Employee

```
Leave Policy Assignment:
- employee: "EMP-001"
- leave_policy: "Standard Policy"
- effective_from: 2026-01-01
- effective_to: 2026-12-31
- carry_forward: ✓ (checked)
```

### Step 4: Result

-   Leave Allocation created automatically
-   On January 1, 2026: 2.5 days added (30 / 12)
-   On February 1, 2026: 2.5 days added
-   On March 1, 2026: 2.5 days added
-   ... and so on

---

## Notes

-   **Scheduler runs daily** but only allocates on `allocate_on_day`
-   **Leave Policy Assignment is required** for automatic allocation
-   **annual_allocation** in Leave Policy Detail is used for calculation
-   **total_leaves_allocated** is updated automatically, not `new_leaves_allocated`
-   **Leave Ledger Entry** is created for each allocation
-   **Comment** is added to Leave Allocation with allocation details
-   **Carry forward** works with Earned Leaves if enabled in Leave Type

---

## Key Functions

-   `allocate_earned_leaves()`: Main scheduler function in `hrms/hr/utils.py`
-   `get_earned_leaves()`: Gets Leave Types where `is_earned_leave = 1`
-   `get_monthly_earned_leave()`: Calculates earned leaves based on frequency
-   `check_effective_date()`: Validates if allocation should run today
-   `update_previous_leave_allocation()`: Updates existing allocation with new leaves
