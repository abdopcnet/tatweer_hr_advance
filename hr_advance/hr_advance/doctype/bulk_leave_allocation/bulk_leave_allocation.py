# Copyright (c) 2025, Hadeel Milad and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, flt, getdate

from hrms.hr.doctype.leave_allocation.leave_allocation import get_carry_forwarded_leaves


class BulkLeaveallocation(Document):
    pass


@frappe.whitelist()
def get_active_employees(company, leave_type, from_date, to_date, department=None, yearly_leave_type=0):
    """
    Get active employees with their leave balances
    """
    if not company or not leave_type or not from_date or not to_date:
        frappe.throw(
            _("Company, Leave Type, From Date, and To Date are required"))

    # Validate dates
    from_date_obj = getdate(from_date)
    to_date_obj = getdate(to_date)
    if date_diff(to_date_obj, from_date_obj) <= 0:
        frappe.throw(_("To date cannot be before from date"))

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
        fields=["name", "employee_name", "department", "company"],
        order_by="employee_name",
    )

    # Determine carry_forward and new_leaves_allocated based on yearly_leave_type
    yearly_leave_type = int(yearly_leave_type) if yearly_leave_type else 0
    default_carry_forward = 0 if yearly_leave_type == 0 else 1
    default_new_leaves_allocated = 0.0

    result = []
    for employee in employees:
        # Get unused leaves (carry forward balance) from previous allocations
        # Only if carry_forward is enabled
        unused_leaves = 0.0
        if default_carry_forward == 1:
            try:
                unused_leaves = get_carry_forwarded_leaves(
                    employee.name,
                    leave_type,
                    from_date_obj,
                    carry_forward=True,
                )
                if unused_leaves is None:
                    unused_leaves = 0.0
            except Exception:
                unused_leaves = 0.0

        # Total = unused_leaves (carry forward) + new_leaves_allocated
        total_leaves_allocated = flt(
            unused_leaves, 2) + flt(default_new_leaves_allocated, 2)

        result.append(
            {
                "employee": employee.name,
                "employee_name": employee.employee_name,
                "department": employee.department or "",
                "company": employee.company,
                "leave_type": leave_type,
                "from_date": from_date,
                "to_date": to_date,
                "new_leaves_allocated": default_new_leaves_allocated,
                "carry_forward": default_carry_forward,
                "total_leaves_allocated": flt(total_leaves_allocated, 2),
            }
        )

    return result


@frappe.whitelist()
def create_bulk_leave_allocations(bulk_allocation_name):
    """
    Create Leave Allocation documents in background for all employees in the bulk allocation
    """
    try:
        if not bulk_allocation_name:
            frappe.throw(_("Bulk Allocation document name is required"))

        # Get the bulk allocation document
        bulk_doc = frappe.get_doc(
            "Bulk Leave allocation", bulk_allocation_name)

        if not bulk_doc.bulk_leave_allocation_table or len(bulk_doc.bulk_leave_allocation_table) == 0:
            frappe.throw(_("No employees found in the table"))

        success_count = 0
        failed_count = 0
        failed = []

        for row in bulk_doc.bulk_leave_allocation_table:
            try:
                # Validate dates
                from_date = getdate(row.from_date or bulk_doc.from_date)
                to_date = getdate(row.to_date or bulk_doc.to_date)

                if date_diff(to_date, from_date) <= 0:
                    raise ValueError(_("To date cannot be before from date"))

                # Check if allocation already exists
                existing = frappe.db.exists(
                    "Leave Allocation",
                    {
                        "employee": row.employee,
                        "leave_type": row.leave_type or bulk_doc.leave_type,
                        "from_date": from_date,
                        "to_date": to_date,
                        "docstatus": ("!=", 2),  # Not cancelled
                    },
                )
                if existing:
                    raise ValueError(
                        _("Leave Allocation already exists for this employee and period"))

                # Create Leave Allocation document
                leave_allocation = frappe.new_doc("Leave Allocation")
                leave_allocation.employee = row.employee
                leave_allocation.leave_type = row.leave_type or bulk_doc.leave_type
                leave_allocation.from_date = from_date
                leave_allocation.to_date = to_date
                leave_allocation.new_leaves_allocated = flt(
                    row.new_leaves_allocated, 2)
                leave_allocation.carry_forward = row.carry_forward if row.carry_forward is not None else 1

                # Calculate total leaves allocated
                leave_allocation.set_total_leaves_allocated()

                # Save and submit
                leave_allocation.insert(ignore_permissions=True)
                leave_allocation.submit()

                success_count += 1
            except Exception as e:
                # Individual employee errors - don't log, just collect
                failed_count += 1
                error_msg = str(e)
                failed.append(
                    {
                        "employee": row.employee,
                        "employee_name": row.employee_name or row.employee,
                        "error": error_msg,
                    }
                )

        return {
            "success_count": success_count,
            "failed_count": failed_count,
            "failed": failed,
        }
    except Exception as e:
        # Function failed completely - log error
        frappe.log_error(
            "[bulk_leave_allocation.py] method: create_bulk_leave_allocations",
            "Bulk Leave Allocation",
        )
        frappe.throw(_("Error creating bulk leave allocations"))
