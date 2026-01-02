# Copyright (c) 2026, Hadeel Milad and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, get_link_to_form


class BulkLeavePolicyAssignment(Document):
    pass


@frappe.whitelist()
def get_active_employees(company, leave_policy, assignment_based_on, effective_from, effective_to, leave_period=None, department=None):
    """
    Get active employees for bulk leave policy assignment
    """
    if not company or not leave_policy or not effective_from or not effective_to:
        frappe.throw(_("Please provide all required fields"))

    # Validate dates
    from_date_obj = getdate(effective_from)
    to_date_obj = getdate(effective_to)

    if date_diff(to_date_obj, from_date_obj) <= 0:
        frappe.throw(
            _("Effective To date cannot be before Effective From date"))

    # Build filters for employees
    filters = {
        "status": "Active",
        "company": company,
    }
    if department:
        filters["department"] = department

    # Get active employees
    employees = frappe.get_all(
        "Employee",
        filters=filters,
        fields=["name", "employee_name", "department",
                "company", "date_of_joining"],
        order_by="employee_name",
    )

    result = []
    for employee in employees:
        # Check if assignment already exists for this employee
        existing_filters = {
            "employee": employee.name,
            "leave_policy": leave_policy,
            "docstatus": 1,
            "effective_to": (">=", from_date_obj),
            "effective_from": ("<=", to_date_obj),
        }
        existing = frappe.db.exists(
            "Leave Policy Assignment", existing_filters)

        result.append({
            "employee": employee.name,
            "employee_name": employee.employee_name,
            "department": employee.department or "",
            "company": employee.company or "",
            "date_of_joining": employee.date_of_joining,
            "has_existing_assignment": 1 if existing else 0,
        })

    return result


@frappe.whitelist()
def create_bulk_leave_policy_assignments(bulk_assignment_name):
    """
    Create Leave Policy Assignment documents for all employees in the bulk assignment
    """
    try:
        if not bulk_assignment_name:
            frappe.throw(_("Document name is required"))

        # Get the bulk assignment document
        bulk_doc = frappe.get_doc(
            "Bulk Leave Policy Assignment", bulk_assignment_name)

        if not bulk_doc.bulk_leave_policy_assignment_table or len(bulk_doc.bulk_leave_policy_assignment_table) == 0:
            frappe.throw(_("No employees in the table"))

        # Validate required fields
        if not bulk_doc.company:
            frappe.throw(_("Company is required"))
        if not bulk_doc.leave_policy:
            frappe.throw(_("Leave Policy is required"))
        if not bulk_doc.effective_from:
            frappe.throw(_("Effective From is required"))
        if not bulk_doc.effective_to:
            frappe.throw(_("Effective To is required"))

        # Use dates from bulk doc
        effective_from = getdate(bulk_doc.effective_from)
        effective_to = getdate(bulk_doc.effective_to)

        if date_diff(effective_to, effective_from) <= 0:
            frappe.throw(
                _("Effective To date cannot be before Effective From date"))

        # Determine assignment_based_on
        assignment_based_on = None
        if bulk_doc.assignment_based_on == "Custom Range":
            assignment_based_on = None
        else:
            assignment_based_on = bulk_doc.assignment_based_on

        success_count = 0
        failed_count = 0
        failed = []

        for row in bulk_doc.bulk_leave_policy_assignment_table:
            try:
                # Check if assignment already exists
                existing_filters = {
                    "employee": row.employee,
                    "leave_policy": bulk_doc.leave_policy,
                    "docstatus": 1,
                    "effective_to": (">=", effective_from),
                    "effective_from": ("<=", effective_to),
                }
                existing = frappe.db.exists(
                    "Leave Policy Assignment", existing_filters)

                if existing:
                    raise ValueError(
                        _("Leave Policy Assignment already exists for this employee in this period"))

                # Get employee date of joining
                date_of_joining = frappe.db.get_value(
                    "Employee", row.employee, "date_of_joining")

                # Determine effective_from based on assignment_based_on
                if assignment_based_on == "Joining Date" and date_of_joining:
                    assignment_effective_from = getdate(date_of_joining)
                elif assignment_based_on == "Leave Period" and bulk_doc.leave_period:
                    assignment_effective_from, assignment_effective_to = frappe.db.get_value(
                        "Leave Period", bulk_doc.leave_period, [
                            "from_date", "to_date"]
                    )
                    effective_from = getdate(assignment_effective_from)
                    effective_to = getdate(assignment_effective_to)
                    assignment_effective_from = effective_from
                else:
                    assignment_effective_from = effective_from

                # Create Leave Policy Assignment document
                assignment = frappe.new_doc("Leave Policy Assignment")
                assignment.employee = row.employee
                assignment.leave_policy = bulk_doc.leave_policy
                assignment.assignment_based_on = assignment_based_on
                assignment.effective_from = assignment_effective_from
                assignment.effective_to = effective_to
                assignment.leave_period = bulk_doc.leave_period if assignment_based_on == "Leave Period" else None
                assignment.carry_forward = bulk_doc.carry_forward if bulk_doc.carry_forward is not None else 0

                # Save and submit
                assignment.insert(ignore_permissions=True)
                assignment.submit()

                # Update row status
                frappe.db.set_value(
                    "Bulk Leave Policy Assignment Table",
                    row.name,
                    {
                        "status": "Success",
                        "assignment_name": assignment.name,
                    },
                )

                success_count += 1
            except Exception as e:
                # Individual employee errors - don't log, just collect
                failed_count += 1
                error_msg = str(e)
                failed.append({
                    "employee": row.employee,
                    "employee_name": row.employee_name or row.employee,
                    "error": error_msg,
                })

                # Update row status
                frappe.db.set_value(
                    "Bulk Leave Policy Assignment Table",
                    row.name,
                    {
                        "status": f"Failed: {error_msg}",
                    },
                )

        frappe.db.commit()

        return {
            "success_count": success_count,
            "failed_count": failed_count,
            "failed": failed,
        }
    except Exception as e:
        # Function failed completely - log error
        frappe.log_error(
            "[bulk_leave_policy_assignment.py] method: create_bulk_leave_policy_assignments",
            "Bulk Leave Policy Assignment",
        )
        frappe.throw(_("Error creating bulk leave policy assignments"))
