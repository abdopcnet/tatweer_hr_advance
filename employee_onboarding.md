# Employee Onboarding Guide

## Overview

Step-by-step guide to onboard new employees using Employee Onboarding process.

## Steps

### 1. Create Employee Onboarding

**DocType:** `Employee Onboarding`

**Required Fields:**

-   `job_applicant` (Link): Job Applicant record
-   `job_offer` (Link): Job Offer record
-   `company` (Link): Company name
-   `date_of_joining` (Date): Employee joining date
-   `boarding_begins_on` (Date): Onboarding start date

**Optional Fields:**

-   `employee_onboarding_template` (Link): Template for onboarding activities
-   `department` (Link): Department assignment
-   `designation` (Link): Job designation
-   `employee_grade` (Link): Employee grade
-   `holiday_list` (Link): Holiday list for employee

**Location:** HR → Employee Onboarding → New

---

### 2. Submit Employee Onboarding

**Process:**

1. Fill required fields
2. Select employee_onboarding_template (optional)
3. Submit document
4. System automatically:
    - Creates Project for onboarding
    - Creates Tasks from template activities
    - Assigns tasks to users/roles
    - Sets boarding_status to "Pending"

---

### 3. Complete Onboarding Activities

**Child Table:** `activities` (Employee Boarding Activity)

**Fields:**

-   `activity_name` (Data): Activity description
-   `user` (Link): Assigned user
-   `role` (Link): Assigned role
-   `task` (Link): Linked Task (auto-created)
-   `required_for_employee_creation` (Check): Mandatory for employee creation

**Process:**

1. Review activities in activities table
2. Complete each task
3. Mark tasks as "Completed" in Task list
4. System updates activity status

---

### 4. Create Employee

**Button:** "Make Employee"

**Requirements:**

-   All tasks with `required_for_employee_creation = 1` must be completed
-   Employee Onboarding must be submitted

**Process:**

1. Complete all required activities
2. Click "Make Employee" button
3. System creates Employee record with:
    - `employee_name` from job_applicant
    - `status = "Active"`
    - `personal_email` from job_applicant
    - Other fields from Employee Onboarding
4. Employee Onboarding.employee field is auto-filled

---

## Field Reference

### Employee Onboarding Fields

-   `tabEmployee Onboarding.job_applicant`: Job Applicant link
-   `tabEmployee Onboarding.job_offer`: Job Offer link
-   `tabEmployee Onboarding.company`: Company assignment
-   `tabEmployee Onboarding.date_of_joining`: Joining date
-   `tabEmployee Onboarding.boarding_begins_on`: Onboarding start date
-   `tabEmployee Onboarding.employee_onboarding_template`: Template link
-   `tabEmployee Onboarding.department`: Department assignment
-   `tabEmployee Onboarding.designation`: Designation assignment
-   `tabEmployee Onboarding.employee_grade`: Grade assignment
-   `tabEmployee Onboarding.holiday_list`: Holiday list
-   `tabEmployee Onboarding.boarding_status`: Status (Pending/In Process/Completed)
-   `tabEmployee Onboarding.project`: Auto-created Project link
-   `tabEmployee Onboarding.activities`: Activities table

### Employee Boarding Activity Fields (Child Table)

-   `tabEmployee Boarding Activity.activity_name`: Activity description
-   `tabEmployee Boarding Activity.user`: Assigned user
-   `tabEmployee Boarding Activity.role`: Assigned role
-   `tabEmployee Boarding Activity.task`: Linked Task
-   `tabEmployee Boarding Activity.required_for_employee_creation`: Mandatory flag

---

## Onboarding Template

### Create Template

**DocType:** `Employee Onboarding Template`

**Fields:**

-   `company` (Link): Company name
-   `department` (Link): Default department
-   `designation` (Link): Default designation
-   `employee_grade` (Link): Default grade
-   `activities` (Table): List of activities

**Usage:**

-   Create template with standard activities
-   Select template in Employee Onboarding
-   Activities are auto-populated from template

---

## Quick Setup Checklist

-   [ ] Create Job Applicant record
-   [ ] Create Job Offer record
-   [ ] Create Employee Onboarding with job_applicant and job_offer
-   [ ] Select employee_onboarding_template (optional)
-   [ ] Fill company, date_of_joining, boarding_begins_on
-   [ ] Submit Employee Onboarding
-   [ ] Complete all required activities
-   [ ] Mark tasks as "Completed"
-   [ ] Click "Make Employee" button
-   [ ] Verify Employee record created
-   [ ] Assign Leave Policy to new employee
-   [ ] Assign Salary Structure to new employee

---

## Notes

-   Employee Onboarding must be submitted before activities are created
-   Project and Tasks are created automatically on submit
-   All required_for_employee_creation activities must be completed before creating Employee
-   Employee Onboarding.employee field is auto-filled after Employee creation
-   Onboarding template helps standardize the onboarding process
-   boarding_status updates automatically as tasks are completed
