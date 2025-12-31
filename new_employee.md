# New Employee Setup Guide

## Overview

Step-by-step guide to create and setup a new employee in HRMS.

## Steps

### 1. Create Employee Record

**DocType:** `Employee`

**Required Fields:**

-   `employee_name` (Data): Full name of employee
-   `company` (Link): Company name
-   `date_of_joining` (Date): Employee joining date
-   `status` (Select): Set to "Active"

**Optional Fields:**

-   `department` (Link): Department
-   `designation` (Link): Job designation
-   `grade` (Link): Employee grade
-   `holiday_list` (Link): Holiday list for employee
-   `user_id` (Link): Link to User account

**Location:** HR → Employee → New

---

### 2. Employee Onboarding (Optional)

**DocType:** `Employee Onboarding`

**Required Fields:**

-   `job_applicant` (Link): Link to Job Applicant
-   `job_offer` (Link): Link to Job Offer
-   `company` (Link): Company name
-   `date_of_joining` (Date): Joining date
-   `boarding_begins_on` (Date): Onboarding start date

**Optional Fields:**

-   `employee_onboarding_template` (Link): Template for onboarding
-   `department` (Link): Department
-   `designation` (Link): Designation
-   `employee_grade` (Link): Employee grade
-   `holiday_list` (Link): Holiday list

**Process:**

1. Submit Employee Onboarding document
2. System creates Project and Tasks automatically
3. Complete all required activities
4. Create Employee from Employee Onboarding using "Make Employee" button

**Location:** HR → Employee Onboarding → New

---

### 3. Assign Leave Policy

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

1. Select employee and leave policy
2. Set effective dates
3. Submit document
4. System automatically creates Leave Allocation documents

**Location:** HR → Leave Policy Assignment → New

---

### 4. Assign Salary Structure

**DocType:** `Salary Structure Assignment`

**Required Fields:**

-   `employee` (Link): Employee name
-   `salary_structure` (Link): Salary Structure to assign
-   `from_date` (Date): Assignment start date
-   `company` (Link): Company name

**Optional Fields:**

-   `base` (Currency): Base salary amount
-   `variable` (Currency): Variable pay amount
-   `income_tax_slab` (Link): Tax slab for employee
-   `payroll_payable_account` (Link): Account for payroll
-   `payroll_cost_centers` (Table): Cost center distribution

**Process:**

1. Select employee and salary structure
2. Set from_date (usually date_of_joining)
3. Enter base and variable amounts if needed
4. Submit document

**Location:** Payroll → Salary Structure Assignment → New

---

## Field Reference

### Employee Fields

-   `tabEmployee.employee_name`: Employee full name
-   `tabEmployee.company`: Company assignment
-   `tabEmployee.date_of_joining`: Joining date
-   `tabEmployee.status`: Employee status (Active/Inactive/Left)
-   `tabEmployee.department`: Department assignment
-   `tabEmployee.designation`: Job designation
-   `tabEmployee.grade`: Employee grade
-   `tabEmployee.holiday_list`: Holiday list for attendance

### Leave Policy Assignment Fields

-   `tabLeave Policy Assignment.employee`: Employee link
-   `tabLeave Policy Assignment.leave_policy`: Policy to assign
-   `tabLeave Policy Assignment.effective_from`: Start date
-   `tabLeave Policy Assignment.effective_to`: End date
-   `tabLeave Policy Assignment.carry_forward`: Carry forward flag

### Salary Structure Assignment Fields

-   `tabSalary Structure Assignment.employee`: Employee link
-   `tabSalary Structure Assignment.salary_structure`: Structure to assign
-   `tabSalary Structure Assignment.from_date`: Assignment start date
-   `tabSalary Structure Assignment.base`: Base salary
-   `tabSalary Structure Assignment.variable`: Variable pay

---

## Quick Setup Checklist

-   [ ] Create Employee record with basic details
-   [ ] Set employee status to "Active"
-   [ ] Assign Leave Policy (creates Leave Allocations automatically)
-   [ ] Assign Salary Structure
-   [ ] Verify Leave Allocations created
-   [ ] Link User account if needed (for login access)

---

## Notes

-   Employee Onboarding is optional but recommended for structured onboarding
-   Leave Policy Assignment automatically creates Leave Allocation documents on submit
-   Salary Structure Assignment must be submitted before payroll processing
-   Employee must be Active to appear in payroll and leave applications
