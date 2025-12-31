# Leave Policy Setup Guide

## Overview

Step-by-step guide to create and configure Leave Policy for employees.

## Steps

### 1. Create Leave Policy

**DocType:** `Leave Policy`

**Required Fields:**

-   `title` (Data): Policy name/title

**Child Table:** `leave_policy_details` (Leave Policy Detail)

**Location:** HR → Leave Policy → New

---

### 2. Add Leave Types to Policy

**Child Table:** `leave_policy_details`

**Required Fields (per row):**

-   `leave_type` (Link): Leave Type name
-   `annual_allocation` (Float): Number of days allocated per year

**Process:**

1. Click "Add Row" in leave_policy_details table
2. Select leave_type from dropdown
3. Enter annual_allocation (e.g., 30 for 30 days per year)
4. Repeat for each leave type
5. Submit Leave Policy document

**Example:**

-   Leave Type: "Annual Leave", annual_allocation: 30
-   Leave Type: "Sick Leave", annual_allocation: 12

---

### 3. Assign Policy to Employee

**DocType:** `Leave Policy Assignment`

**Required Fields:**

-   `employee` (Link): Employee name
-   `leave_policy` (Link): Leave Policy to assign
-   `effective_from` (Date): Policy start date
-   `effective_to` (Date): Policy end date

**Optional Fields:**

-   `assignment_based_on` (Select):
    -   "Leave Period": Use Leave Period dates
    -   "Joining Date": Use employee joining date
-   `leave_period` (Link): Required if assignment_based_on = "Leave Period"
-   `carry_forward` (Check): Enable carry forward of unused leaves

**Process:**

1. Select employee
2. Select leave_policy
3. Set effective_from and effective_to dates
4. Enable carry_forward if needed
5. Submit document
6. System automatically creates Leave Allocation documents

**Location:** HR → Leave Policy Assignment → New

---

## Field Reference

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
-   `tabLeave Policy Assignment.assignment_based_on`: Assignment method
-   `tabLeave Policy Assignment.leave_period`: Leave Period (if applicable)
-   `tabLeave Policy Assignment.carry_forward`: Carry forward flag

---

## Earned Leaves Configuration

### For Earned Leave Types

**Leave Type Settings:**

-   `tabLeave Type.is_earned_leave` = 1
-   `tabLeave Type.earned_leave_frequency` = "Monthly" (or Quarterly, Half-Yearly, Yearly)
-   `tabLeave Type.allocate_on_day` = "First Day" (or "Last Day", "Date of Joining")

**Leave Policy Detail:**

-   Set `annual_allocation` in Leave Policy Detail
-   Example: 30 days annual = 2.5 days per month (30/12)

**Automatic Allocation:**

-   Scheduler runs daily: `hrms.hr.utils.allocate_earned_leaves`
-   Adds earned_leaves on allocate_on_day
-   Formula: `earned_leaves = annual_allocation / 12` (for Monthly)

---

## Quick Setup Checklist

-   [ ] Create Leave Policy with title
-   [ ] Add leave types to leave_policy_details table
-   [ ] Set annual_allocation for each leave type
-   [ ] Submit Leave Policy
-   [ ] Assign policy to employee via Leave Policy Assignment
-   [ ] Verify Leave Allocations created automatically
-   [ ] Check earned leaves allocation (if applicable)

---

## Notes

-   Leave Policy must be submitted before assignment
-   Leave Policy Assignment automatically creates Leave Allocation on submit
-   For earned leaves, ensure Leave Type has is_earned_leave = 1
-   annual_allocation in Leave Policy Detail is used for earned leaves calculation
-   carry_forward in Leave Policy Assignment enables unused leaves carry forward
