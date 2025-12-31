# Salary Structure Setup Guide

## Overview

Step-by-step guide to create and assign Salary Structure for employees.

## Steps

### 1. Create Salary Structure

**DocType:** `Salary Structure`

**Required Fields:**

-   `company` (Link): Company name
-   `payroll_frequency` (Select): Monthly, Fortnightly, Bimonthly, Weekly, Daily
-   `is_active` (Select): Yes/No

**Child Tables:**

-   `earnings` (Salary Detail): Earning components
-   `deductions` (Salary Detail): Deduction components

**Location:** Payroll → Salary Structure → New

---

### 2. Add Salary Components

**Child Table:** `earnings` or `deductions`

**Required Fields (per row):**

-   `salary_component` (Link): Salary Component name
-   `amount` (Currency): Fixed amount (or use formula)
-   `formula` (Small Text): Formula for calculation (optional)

**Process:**

1. Click "Add Row" in earnings or deductions table
2. Select salary_component
3. Enter amount or formula
4. Repeat for all components
5. Submit Salary Structure

**Example Earnings:**

-   Basic Salary: amount = 5000
-   House Rent Allowance: formula = `base * 0.4`
-   Transport Allowance: amount = 500

**Example Deductions:**

-   Provident Fund: formula = `base * 0.12`
-   Professional Tax: amount = 200

---

### 3. Assign to Employee

**DocType:** `Salary Structure Assignment`

**Required Fields:**

-   `employee` (Link): Employee name
-   `salary_structure` (Link): Salary Structure to assign
-   `from_date` (Date): Assignment start date
-   `company` (Link): Company name

**Optional Fields:**

-   `base` (Currency): Base salary amount (overrides structure base)
-   `variable` (Currency): Variable pay amount
-   `income_tax_slab` (Link): Tax slab for employee
-   `payroll_payable_account` (Link): Account for payroll payments
-   `payroll_cost_centers` (Table): Cost center distribution percentages

**Process:**

1. Select employee
2. Select salary_structure
3. Set from_date (usually date_of_joining)
4. Enter base and variable if different from structure
5. Set income_tax_slab if applicable
6. Add payroll_cost_centers if needed
7. Submit document

**Location:** Payroll → Salary Structure Assignment → New

---

## Field Reference

### Salary Structure Fields

-   `tabSalary Structure.company`: Company assignment
-   `tabSalary Structure.payroll_frequency`: Payroll frequency
-   `tabSalary Structure.is_active`: Active status
-   `tabSalary Structure.earnings`: Earning components table
-   `tabSalary Structure.deductions`: Deduction components table

### Salary Detail Fields (Child Table)

-   `tabSalary Detail.salary_component`: Component name
-   `tabSalary Detail.amount`: Fixed amount
-   `tabSalary Detail.formula`: Calculation formula
-   `tabSalary Detail.condition`: Conditional formula

### Salary Structure Assignment Fields

-   `tabSalary Structure Assignment.employee`: Employee link
-   `tabSalary Structure Assignment.salary_structure`: Structure to assign
-   `tabSalary Structure Assignment.from_date`: Assignment start date
-   `tabSalary Structure Assignment.base`: Base salary override
-   `tabSalary Structure Assignment.variable`: Variable pay
-   `tabSalary Structure Assignment.income_tax_slab`: Tax slab
-   `tabSalary Structure Assignment.payroll_payable_account`: Payment account
-   `tabSalary Structure Assignment.payroll_cost_centers`: Cost centers table

---

## Formula Examples

### Percentage of Base

```
base * 0.4
```

### Conditional Formula

```
base if base > 10000 else base * 0.3
```

### Component Reference

```
base + house_rent_allowance
```

### Date-based Calculation

```
base if date_of_joining < "2024-01-01" else base * 1.1
```

---

## Quick Setup Checklist

-   [ ] Create Salary Structure with company and frequency
-   [ ] Add earning components to earnings table
-   [ ] Add deduction components to deductions table
-   [ ] Set formulas or amounts for each component
-   [ ] Submit Salary Structure
-   [ ] Assign to employee via Salary Structure Assignment
-   [ ] Set from_date (usually date_of_joining)
-   [ ] Enter base and variable if needed
-   [ ] Set income_tax_slab if applicable
-   [ ] Submit Salary Structure Assignment

---

## Notes

-   Salary Structure must be submitted before assignment
-   from_date in Salary Structure Assignment should match employee date_of_joining
-   base and variable in assignment override structure defaults
-   payroll_payable_account is required for payroll processing
-   payroll_cost_centers distributes salary across cost centers
-   Only one active Salary Structure Assignment per employee at a time
