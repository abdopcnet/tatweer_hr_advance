
# from erpnext.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
import frappe
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.hr.doctype.shift_assignment.shift_assignment import get_actual_start_end_datetime_of_shift
from frappe.model.document import Document
import datetime
import math
from frappe.utils import now, cint, get_datetime, getdate
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day
from frappe import _

from hr_advance.api import get_additional_salaries  # New Function


class overrid_salary_slip(SalarySlip):

    # change the filed bank account to be form the new custom filed in the employee doctype
    def pull_emp_details(self):
        account_details = frappe.get_cached_value(
            "Employee", self.employee, ["custom_bank_name", "bank_ac_no", "salary_mode"], as_dict=1
        )
        if account_details:
            self.mode_of_payment = account_details.salary_mode
            self.bank_name = account_details.custom_bank_name
            self.bank_account_no = account_details.bank_ac_no

    def set_salary_structure_assignment(self):
        self.custom_responsibility_bonus = 0.000
        self.custom_fuel_and_communications_allowance = 0.000
        self.custom_distinction_bonus = 0.000

        self._salary_structure_assignment = frappe.db.get_value(
            "Salary Structure Assignment",
            {
                "employee": self.employee,
                "salary_structure": self.salary_structure,
                "from_date": ("<=", self.actual_start_date),
                "docstatus": 1,
            },
            "*",
            order_by="from_date desc",
            as_dict=True,
        )
        try:

            employee = frappe.get_doc("Employee", self.employee)
            designation = frappe.get_doc("Designation", employee.designation)
            designation_type = frappe.get_doc(
                "Designation Type", employee.custom_designation_type)

            # self.custom_responsibility_bonus = 90
            if designation:
                if designation.custom_is_it_a_leadership_position:
                    self.custom_responsibility_bonus = designation.custom_responsibility_bonus or designation_type.responsibility_bonus
                    self.custom_fuel_and_communications_allowance = designation.custom_fuel_and_communications_allowance or designation_type.fuel_and_communications_allowance
                else:
                    self.custom_distinction_bonus = designation.custom_distinction_bonus or designation_type.distinction_bonus
        except Exception as e:
            frappe.log_error(
                "[salary_slip.py] method: set_salary_structure_assignment",
                "Salary Slip",
            )
            frappe.msgprint(
                _("Can not fetch Bonus Value value from Employee Designation Info"))

        if not self._salary_structure_assignment:
            frappe.throw(
                _(
                    "Please assign a Salary Structure for Employee {0} applicable from or before {1} first"
                ).format(
                    frappe.bold(self.employee_name),
                    frappe.bold(formatdate(self.actual_start_date)),
                )
            )

    # def add_additional_salary_components(self, component_type):
    # 	from hrms.payroll.doctype.salary_slip.salary_slip import get_salary_component_data

    # 	additional_salaries = get_additional_salaries(
    # 		self.employee, self.start_date, self.end_date, component_type
    # 	)

    # 	for additional_salary in additional_salaries:
    # 		self.update_component_row(
    # 			get_salary_component_data(additional_salary.component),
    # 			additional_salary.amount,
    # 			additional_salary.amount,
    # 			component_type,
    # 			additional_salary,
    # 			is_recurring=additional_salary.is_recurring,
    # 		)

    def add_additional_salary_components(self, component_type):
        additional_salaries = get_additional_salaries(
            self.employee, self.start_date, self.end_date, component_type
        )

        for additional_salary in additional_salaries:
            component_data = get_salary_component_data(
                additional_salary.component)
            self.update_component_row(
                component_data,
                additional_salary.amount,
                component_type,
                additional_salary,
                is_recurring=additional_salary.is_recurring,
            )

            if component_type == "earnings" and hasattr(self, "benefit_ledger_components"):
                if (
                        additional_salary.ref_doctype == "Employee Benefit Claim"
                        and component_data.is_flexible_benefit
                ) or component_data.accrual_component:
                    # track benefit claim or accrual component payout to record in Employee Benefit Ledger
                    if additional_salary.ref_doctype == "Employee Benefit Claim":
                        remarks = f"Payout against Employee Benefit Claim {additional_salary.ref_docname}"
                        flexible_benefit = 1
                    else:
                        remarks = "Accrual Component payout via Additional Salary"
                        flexible_benefit = 0

                    self.benefit_ledger_components.append(
                        {
                            "salary_component": additional_salary.component,
                            "amount": additional_salary.amount,
                            "is_accrual": 0,
                            "transaction_type": "Payout",
                            "flexible_benefit": flexible_benefit,
                            "remarks": remarks,
                        }
                    )


def get_salary_component_data(component):
    # get_cached_value doesn't work here due to alias "name as salary_component"
    return frappe.db.get_value(
        "Salary Component",
        component,
        (
            "name as salary_component",
            "depends_on_payment_days",
            "salary_component_abbr as abbr",
            "do_not_include_in_total",
            # "do_not_include_in_accounts",
            "is_tax_applicable",
            "is_flexible_benefit",
            "variable_based_on_taxable_salary",
            # "accrual_component",
        ),
        as_dict=1,
        cache=True,
    )
