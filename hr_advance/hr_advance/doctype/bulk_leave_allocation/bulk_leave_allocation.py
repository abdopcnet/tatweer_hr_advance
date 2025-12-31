# Copyright (c) 2025, Hadeel Milad and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate

from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on


class BulkLeaveallocation(Document):
    pass


@frappe.whitelist()
def get_active_employees(company, leave_type, from_date, to_date, department=None):
    """
    Get active employees with their leave balances
    """
    if not company or not leave_type or not from_date or not to_date:
        frappe.throw(
            _("Company, Leave Type, From Date, and To Date are required"))

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

    result = []
    for employee in employees:
        # Get current leave balance
        try:
            leave_balance = get_leave_balance_on(
                employee.name,
                leave_type,
                getdate(from_date),
                getdate(to_date),
            )
            if leave_balance is None:
                leave_balance = 0.0
        except Exception:
            leave_balance = 0.0

        result.append(
            {
                "employee": employee.name,
                "employee_name": employee.employee_name,
                "department": employee.department or "",
                "company": employee.company,
                "leave_type": leave_type,
                "from_date": from_date,
                "to_date": to_date,
                "new_leaves_allocated": 0.0,
                "carry_forward": 0,
                "total_leaves_allocated": flt(leave_balance, 2),
            }
        )

    return result


@frappe.whitelist()
def create_bulk_leave_allocations(bulk_allocation_name):
    """
    Create Leave Allocation documents in background for all employees in the bulk allocation
    """
    if not bulk_allocation_name:
        frappe.throw(_("Bulk Allocation document name is required"))

    # Get the bulk allocation document
    bulk_doc = frappe.get_doc("Bulk Leave allocation", bulk_allocation_name)

    if not bulk_doc.bulk_leave_allocation_table or len(bulk_doc.bulk_leave_allocation_table) == 0:
        frappe.throw(_("No employees found in the table"))

    success_count = 0
    failed_count = 0
    failed = []

    for row in bulk_doc.bulk_leave_allocation_table:
        try:
            # Create Leave Allocation document
            leave_allocation = frappe.new_doc("Leave Allocation")
            leave_allocation.employee = row.employee
            leave_allocation.leave_type = row.leave_type or bulk_doc.leave_type
            leave_allocation.from_date = row.from_date or bulk_doc.from_date
            leave_allocation.to_date = row.to_date or bulk_doc.to_date
            leave_allocation.new_leaves_allocated = flt(
                row.new_leaves_allocated, 2)
            leave_allocation.carry_forward = row.carry_forward or 0

            # Calculate total leaves allocated
            leave_allocation.set_total_leaves_allocated()

            # Save and submit
            leave_allocation.insert(ignore_permissions=True)
            leave_allocation.submit()

            success_count += 1
        except Exception as e:
            failed_count += 1
            failed.append(
                {
                    "employee": row.employee,
                    "employee_name": row.employee_name,
                    "error": str(e),
                }
            )
            frappe.log_error(
                f"[bulk_leave_allocation.py] method: create_bulk_leave_allocations - Employee: {row.employee}",
                "Bulk Leave Allocation",
            )

    return {
        "success_count": success_count,
        "failed_count": failed_count,
        "failed": failed,
    }
