# Copyright (c) 2025, Hadeel Milad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _, msgprint, throw


class EmployeeTrainingRequest(Document):
    def before_save(self):
        try:
            # Get the maximum allowed requests from HR Settings Single DocType
            max_employee_request = frappe.db.get_single_value('HR Settings', 'custom_max_employee_requests')

            # Ensure max_employee_request is a valid integer
            if max_employee_request is None:
                frappe.throw(_("Max Employee Requests setting not found in HR Settings. Please configure it."))
            try:
                max_employee_request = int(max_employee_request)
            except ValueError:
                frappe.throw(_("Max Employee Requests in HR Settings must be a valid number."))

            # Count submitted training requests for the current employee
            # docstatus: 1 means 'Submitted'
            # Adjust filters if 'create records' refers to 'Open', 'Approved', etc.
            employee_requests = frappe.db.get_all(
                "Employee Training Request",
                filters={
                    "employee": self.employee,
                    "docstatus": 0 # Counting submitted requests. Adjust if policy means 'pending' or 'approved'.
                },
                # We only need the count, so fetching 'name' is sufficient.
                # Frappe's get_all is optimized for count when only name is needed implicitly.
                fields=["name"]
            )

            # Check if the number of requests exceeds the allowed limit
            if len(employee_requests) > max_employee_request:
                # Use the correct, descriptive error message
                frappe.throw(
                    _("This training request cannot be submitted for '{0}', because it exceeds the number of requests allowed according to the company policy. Only '{1}' requests are permitted.").format(
                        self.employee_name, max_employee_request
                    )
                )

        except frappe.ValidationError:
            # Re-raise Frappe ValidationErrors directly
            raise
        except Exception as e:
            # Catch any other unexpected errors during validation logic
            frappe.msgprint(f"An unexpected error occurred during validation: {e}",
                           title="Error", indicator="red")
            frappe.log_error(f"Error in EmployeeTrainingRequest validation for employee {self.employee}: {frappe.get_traceback()}", str(e))
            frappe.throw(_("An internal error occurred during validation. Please contact your system administrator."))