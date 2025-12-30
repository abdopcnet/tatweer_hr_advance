
# from erpnext.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
import frappe
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from hrms.hr.doctype.shift_assignment.shift_assignment import get_actual_start_end_datetime_of_shift
from frappe.model.document import Document
import datetime, math
from frappe.utils import now, cint, get_datetime ,getdate
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day
from frappe import _

import erpnext
from frappe.query_builder.functions import Coalesce, Count

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from erpnext.accounts.utils import get_fiscal_year

from hrms.payroll.doctype.salary_slip.salary_slip_loan_utils import if_lending_app_installed
from hrms.payroll.doctype.salary_withholding.salary_withholding import link_bank_entry_in_salary_withholdings
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	get_link_to_form,
	getdate,
)



class overrid_payroll_entry(PayrollEntry):

    # def set_accounting_entries_for_bank_entry(self, total_je_payment_amount, user_remark):
    #     # Renamed je_payment_amount to total_je_payment_amount for clarity,
    #     # as the individual employee amounts will be calculated within the loop.

    #     payroll_payable_account = self.payroll_payable_account
    #     precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

    #     accounts = []
    #     currencies = []
    #     company_currency = erpnext.get_company_currency(self.company)
    #     accounting_dimensions = get_accounting_dimensions() or []

    #     # --- PART 1: Credit entry for the company's payment account (main bank account) ---
    #     # This will be the total amount for the entire payroll entry.
    #     exchange_rate_credit, amount_credit = self.get_amount_and_exchange_rate_for_journal_entry(
    #         self.payment_account, total_je_payment_amount, company_currency, currencies
    #     )
    #     accounts.append(
    #         self.update_accounting_dimensions(
    #             {
    #                 "account": self.payment_account,
    #                 "bank_account": self.bank_account, # This is the Payroll Entry's main bank_account (source bank)
    #                 "credit_in_account_currency": flt(amount_credit, precision),
    #                 "exchange_rate": flt(exchange_rate_credit),
    #                 "cost_center": self.cost_center,
    #             },
    #             accounting_dimensions,
    #         )
    #     )

    #     # --- PART 2: Debit entries for individual employees, grouped by their bank details for logging/remark ---
    #     if self.employee_based_payroll_payable_entries:
    #         # This dictionary is now purely for structuring the remark/logging, not for grouping JE lines
    #         grouped_bank_info_for_remark = {}

    #         for employee, employee_details in self.employee_based_payroll_payable_entries.items():
    #             frappe.log_error(f"Debugging employee_details for {employee}: {employee_details}", "Payroll Entry Bank Grouping Debug")
    #             employee_payment_amount = (
    #                 (employee_details.get("earnings", 0) or 0)
    #                 - (employee_details.get("deductions", 0) or 0)
    #                 - (employee_details.get("total_loan_repayment", 0) or 0)
    #             )

    #             # Get bank details directly from employee_details (payment slip)
    #             emp_slip = frappe.db.get_all("Salary Slip" , filters={'payroll_entry' :['=' , self.name] , 'employee' : [ '=' ,employee]})[0]
    #             bank_name = frappe.db.get_value("Salary Slip" , emp_slip , 'bank_name')
    #             bank_branch =  frappe.db.get_value("Salary Slip" , emp_slip , 'custom_bank_branch')
    #             # bank_name = employee_details.get("bank_name")
    #             # bank_branch = employee_details.get("custom_bank_branch")
                
    #             # Fallback for missing info in slip
    #             bank_name = bank_name if bank_name else "UNKNOWN_ACCOUNT"
    #             bank_branch = bank_branch if bank_branch else "UNKNOWN_BRANCH"

    #             # Calculate exchange rate and amount for this individual employee's debit
    #             # Use payroll_payable_account for debit side
    #             exchange_rate_debit, amount_debit = self.get_amount_and_exchange_rate_for_journal_entry(
    #                 payroll_payable_account, employee_payment_amount, company_currency, currencies
    #             )

    #             # Get employee's specific cost centers for this payment, if applicable
    #             # The original method uses get_payroll_cost_centers_for_employee for this.
    #             # If you group this, the JE line for payroll payable won't be as granular by cost center.
    #             # For this example, we'll use the main self.cost_center for simplicity if no specific employee cost center is passed via `employee_details`.
    #             # If `employee_details` contains a "cost_center", use that. Otherwise, fallback to self.cost_center.
                
    #             # Check if employee_details has a cost_center specific to this employee's payment
    #             employee_specific_cost_center = employee_details.get("cost_center", self.cost_center)


    #             accounts.append(
    #                 self.update_accounting_dimensions(
    #                     {
    #                         "account": payroll_payable_account,
    #                         "debit_in_account_currency": flt(amount_debit, precision),
    #                         "exchange_rate": flt(exchange_rate_debit),
    #                         "reference_type": self.doctype, # Payroll Entry
    #                         "reference_name": self.name,    # Payroll Entry Name
    #                         "party_type": "Employee",       # Link to the employee
    #                         "party": employee,
    #                         "cost_center": employee_specific_cost_center, # Use employee's cost center if available
    #                         # Add employee's bank details for better traceability in the JE line (if needed by your Chart of Accounts)
    #                         # Note: These are custom fields, not standard JE Account fields.
    #                         # They won't directly create accounting entries but can be stored as remarks/notes.
    #                         # Consider adding custom fields to Journal Entry Account if you need structured storage.
    #                         "user_remark": _("Payment for employee {0} via Bank A/c: {1}, Branch: {2}").format(
    #                             employee, bank_name, bank_branch
    #                         )
    #                     },
    #                     accounting_dimensions,
    #                 )
    #             )

    #             # Store info for aggregated remark (if desired)
    #             group_key = (bank_name, bank_branch)
    #             if group_key not in grouped_bank_info_for_remark:
    #                 grouped_bank_info_for_remark[group_key] = []
    #                 # Corrected frappe.format usage for the remark string:
    #             formatted_amount = frappe.format(
    #                 employee_payment_amount,
    #                 {"fieldtype": "Currency", "precision": precision}, # Pass a dict for df, and pass precision
    #                 currency=company_currency # Crucial for proper currency formatting
    #             )
    #             grouped_bank_info_for_remark[group_key].append(
    #                 _("Employee {0} (Amount: {1})").format(employee, formatted_amount)
    #             )

    #             # grouped_bank_info_for_remark[group_key].append(
    #             #     _("Employee {0} (Amount: {1})").format(employee, frappe.format(employee_payment_amount, precision))
    #             #     _("Employee {0} (Amount: {1})").format(employee, frappe.format(employee_payment_amount, None, None, None, precision=precision))
    #             # )

    #         # --- Construct final user_remark with grouped employee info ---
    #         remark_details = []
    #         for group_key, employee_list_remarks in grouped_bank_info_for_remark.items():
    #             bank_acc, bank_br = group_key
    #             remark_details.append(f"\nBank Name: {bank_acc}, Branch: {bank_br}:\n  " + "\n  ".join(employee_list_remarks))

    #         final_user_remark = _("Payment of {0} for payroll period from {1} to {2}").format(
    #             _(user_remark), self.start_date, self.end_date
    #         )
    #         final_user_remark += "\n\n" + _("Grouped Employee Payments:") + "".join(remark_details)

    #     else:
    #         # Original logic for non-employee based entries (single debit line)
    #         exchange_rate_debit, amount_debit = self.get_amount_and_exchange_rate_for_journal_entry(
    #             payroll_payable_account, total_je_payment_amount, company_currency, currencies
    #         )
    #         accounts.append(
    #             self.update_accounting_dimensions(
    #                 {
    #                     "account": payroll_payable_account,
    #                     "debit_in_account_currency": flt(amount_debit, precision),
    #                     "exchange_rate": flt(exchange_rate_debit),
    #                     "reference_type": self.doctype,
    #                     "reference_name": self.name,
    #                     "cost_center": self.cost_center,
    #                 },
    #                 accounting_dimensions,
    #             )
    #         )
    #         final_user_remark = _("Payment of {0} from {1} to {2}").format(
    #             _(user_remark), self.start_date, self.end_date
    #         )

    #     return self.make_journal_entry(
    #         accounts,
    #         currencies,
    #         voucher_type="Bank Entry",
    #         user_remark=final_user_remark,
    #     )

    @frappe.whitelist()
    def make_bank_entry(self, for_withheld_salaries=False):
        print("lllllllllllllllllll")
        self.check_permission("write")
        self.employee_based_payroll_payable_entries = {}
        process_payroll_accounting_entry_based_on_employee = frappe.db.get_single_value(
            "Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
        )

        salary_slip_total = 0
        salary_details = self.get_salary_slip_details(for_withheld_salaries)

        for salary_detail in salary_details:
            if salary_detail.parentfield == "earnings":
                (
                    is_flexible_benefit,
                    only_tax_impact,
                    create_separate_je,
                    statistical_component,
                    do_not_include_in_total,
                ) = frappe.db.get_value(
                    "Salary Component",
                    salary_detail.salary_component,
                    (
                        "is_flexible_benefit",
                        "only_tax_impact",
                        "create_separate_payment_entry_against_benefit_claim",
                        "statistical_component",
                        "do_not_include_in_total",
                    ),
                    cache=True,
                )
                print(salary_detail)
                print(salary_detail)
                if only_tax_impact != 1 and statistical_component != 1 and do_not_include_in_total != 1:
                    if is_flexible_benefit == 1 and create_separate_je == 1:
                        self.set_accounting_entries_for_bank_entry(
                            salary_detail.amount, salary_detail.salary_component
                        )
                    else:
                        if process_payroll_accounting_entry_based_on_employee:
                            self.set_employee_based_payroll_payable_entries(
                                "earnings",
                                salary_detail.employee,
                                salary_detail.amount,
                                salary_detail.salary_structure,
                            )
                        salary_slip_total += salary_detail.amount

            if salary_detail.parentfield == "deductions":
                statistical_component = frappe.db.get_value(
                    "Salary Component", salary_detail.salary_component, "statistical_component", cache=True
                )
                do_not_include_in_total = frappe.db.get_value(
                    "Salary Component", salary_detail.salary_component, "do_not_include_in_total", cache=True
                )
                if not statistical_component and not do_not_include_in_total:
                    if process_payroll_accounting_entry_based_on_employee:
                        self.set_employee_based_payroll_payable_entries(
                            "deductions",
                            salary_detail.employee,
                            salary_detail.amount,
                            salary_detail.salary_structure,
                        )

                    salary_slip_total -= salary_detail.amount

        total_loan_repayment = self.process_loan_repayments_for_bank_entry(salary_details) or 0
        salary_slip_total -= total_loan_repayment
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        print(salary_slip_total)
        bank_entry = None
        if salary_slip_total > 0:
            remark = "withheld salaries" if for_withheld_salaries else "salaries"
            bank_entry = self.set_accounting_entries_for_bank_entry_(salary_slip_total, remark)

            if for_withheld_salaries:
                link_bank_entry_in_salary_withholdings(salary_details, bank_entry.name)

        return bank_entry


    def set_accounting_entries_for_bank_entry_(self, total_je_payment_amount, user_remark):
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        # This method will now create and submit multiple JEs directly
        # and return a list of their names.

        payroll_payable_account = self.payroll_payable_account
        precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

        company_currency = erpnext.get_company_currency(self.company)
        accounting_dimensions = get_accounting_dimensions() or []

        created_journal_entries = [] # To store names of all created JEs
        accounts = []
        currencies = []

        if self.employee_based_payroll_payable_entries or 1==1:
            # Step 1: Group employee payments by bank name and branch
            # This 'bank_groups' dict will hold aggregated data for each JE to be created
            bank_groups = {} # Key: (bank_name, bank_branch), Value: {'total_amount': X, 'employees': [{'name': emp, 'amount': Y, 'cost_center': Z}]}

            # Pre-fetch all necessary Salary Slip data for optimization
            # Collect all salary slip names first
            salary_slip_names_to_fetch = []
            for employee, employee_details in self.employee_based_payroll_payable_entries.items():
                # Assuming 'salary_slip' key exists in employee_details and holds the name
                if employee_details.get("salary_slip"):
                    salary_slip_names_to_fetch.append(employee_details["salary_slip"])

            salary_slips_data = {}
            if salary_slip_names_to_fetch:
                slips = frappe.db.get_all(
                    "Salary Slip",
                    filters={"name": ("in", salary_slip_names_to_fetch)},
                    fields=["name", "employee", "bank_name", "custom_bank_branch"],
                    as_list=False
                )
                for slip in slips:
                    salary_slips_data[slip.name] = slip

            # Now iterate through payroll entries and build bank_groups
            for employee, employee_details in self.employee_based_payroll_payable_entries.items():
                # Logging from your provided snippet
                # frappe.log_error(f"Debugging employee_details for {employee}: {employee_details}", "Payroll Entry Bank Grouping Debug")
                
                employee_payment_amount = (
                    flt(employee_details.get("earnings", 0))
                    - flt(employee_details.get("deductions", 0))
                    - flt(employee_details.get("total_loan_repayment", 0))
                )

                # bank_name = "UNKNOWN_BANK"
                # bank_branch = "UNKNOWN_BRANCH"

                # Get bank details directly from employee_details (payment slip)
                emp_slip = frappe.db.get_all("Salary Slip" , filters={'payroll_entry' :['=' , self.name] , 'employee' : [ '=' ,employee]})[0]
                bank_name = frappe.db.get_value("Salary Slip" , emp_slip , 'bank_name')
                bank_branch =  frappe.db.get_value("Salary Slip" , emp_slip , 'custom_bank_branch')
                # bank_name = employee_details.get("bank_name")
                # bank_branch = employee_details.get("custom_bank_branch")
                
                # Fallback for missing info in slip
                bank_name = bank_name if bank_name else "UNKNOWN_ACCOUNT"
                bank_branch = bank_branch if bank_branch else "UNKNOWN_BRANCH"

                # # Get bank details from pre-fetched Salary Slip data
                # salary_slip_name = employee_details.get("salary_slip")
                # if salary_slip_name and salary_slip_name in salary_slips_data:
                #     slip_doc_data = salary_slips_data[salary_slip_name]
                #     bank_name = slip_doc_data.get("bank_name") or bank_name
                #     bank_branch = slip_doc_data.get("custom_bank_branch") or bank_branch # Use custom_bank_branch

                group_key = (bank_name, bank_branch)

                if group_key not in bank_groups:
                    bank_groups[group_key] = {
                        "total_amount": 0.0,
                        "employees_info": [] # List of {'employee': name, 'amount': value, 'cost_center': value}
                    }
                
                bank_groups[group_key]["total_amount"] += employee_payment_amount
                bank_groups[group_key]["employees_info"].append({
                    "name": employee, # Renamed 'employee' to 'name' for clarity
                    "amount": employee_payment_amount,
                    "cost_center": employee_details.get("cost_center", self.cost_center)
                })

            # Step 2: Create and submit a Journal Entry for each bank group
            for group_key, group_data in bank_groups.items():
                bank_name_for_je, bank_branch_for_je = group_key
                group_total_amount = group_data["total_amount"]
                employees_in_group = group_data["employees_info"]

                # Create a new Journal Entry document
                new_je = frappe.new_doc("Journal Entry")
                new_je.voucher_type = "Bank Entry"
                new_je.company = self.company
                new_je.posting_date = self.posting_date 
                new_je.reference_no = self.name # Link back to Payroll Entry
                new_je.reference_date = self.posting_date
                new_je.cheque_no = '' # If applicable
                new_je.cheque_date = ''# If applicable
                new_je.project = self.project # If Payroll Entry has a project

                # Construct the remark for this specific JE
                je_remark_title = _("Payroll payment for employees transferring to Bank: {0}, Branch: {1}").format(
                    bank_name_for_je, bank_branch_for_je
                )
                je_remark_period = _("Period from {0} to {1}").format(self.start_date, self.end_date)
                
                # List individual employees and their amounts in the remark
                employee_list_for_remark = []
                for emp_data in employees_in_group:
                    formatted_emp_amount = frappe.format(
                        emp_data['amount'],
                        {"fieldtype": "Currency", "precision": precision},
                        currency=company_currency
                    )
                    employee_list_for_remark.append(
                        _("Employee {0} (Amount: {1})").format(emp_data['name'], formatted_emp_amount)
                    )
                
                new_je.user_remark = f"{je_remark_title}\n{je_remark_period}\n\n{_('Employees in this group:')}\n" + "\n".join(employee_list_for_remark)
                new_je.remark = new_je.user_remark # Also set system remark

                # Add Credit line (from company's payment account)
                # This credit is for the total amount of this specific bank group
                exchange_rate_credit, amount_credit = self.get_amount_and_exchange_rate_for_journal_entry(
                    self.payment_account, group_total_amount, company_currency, [] # Use empty list for currencies here, new_je.get("currencies", []) might not be populated yet
                )
                
                new_je.append("accounts",
                    self.update_accounting_dimensions(
                        {
                            "account": self.payment_account,
                            "bank_account": self.bank_account,
                            "credit_in_account_currency": flt(amount_credit, precision),
                            "exchange_rate": flt(exchange_rate_credit),
                            "cost_center": self.cost_center,
                        },
                        accounting_dimensions,
                        # doc=new_je # Pass the new_je document for context
                    )
                )

                # Add Debit lines (Payroll Payable for each employee in the group)
                for emp_data in employees_in_group:
                    exchange_rate_debit, amount_debit = self.get_amount_and_exchange_rate_for_journal_entry(
                        payroll_payable_account, emp_data['amount'], company_currency, [] # Use empty list for currencies here
                    )
                    new_je.append("accounts",
                        self.update_accounting_dimensions(
                            {
                                "account": payroll_payable_account,
                                "debit_in_account_currency": flt(amount_debit, precision),
                                "exchange_rate": flt(exchange_rate_debit),
                                "reference_type": self.doctype, # Payroll Entry
                                "reference_name": self.name,    # Payroll Entry Name
                                "party_type": "Employee",
                                "party": emp_data['name'],
                                "cost_center": emp_data['cost_center'],
                                "user_remark": _("Payment for employee {0} (Bank: {1}, Branch: {2})").format(
                                    emp_data['name'], bank_name_for_je, bank_branch_for_je
                                )
                            },
                            accounting_dimensions,
                            # doc=new_je # Pass the new_je document for context
                        )
                    )
                
                try:
                    new_je.flags.ignore_mandatory = True
                    new_je.insert()
                    # new_je.submit()
                    created_journal_entries.append(new_je.name)
                    frappe.msgprint(_("Journal Entry {0} created and submitted for Bank: {1}, Branch: {2}").format(
                        new_je.name, bank_name_for_je, bank_branch_for_je))
                except Exception as e:
                    frappe.log_error(f"Error creating/submitting Journal Entry for Bank {bank_name_for_je}, Branch {bank_branch_for_je}: {e}", "Multi-JE Creation Error")
                    frappe.throw(_("Failed to create Journal Entry for a bank group. Please check error log for details."))

            # Optional: Update the Payroll Entry to link to the created JEs
            # You might need a custom field on Payroll Entry, e.g., 'custom_linked_journal_entries' (type Table)
            # Or a simple 'Data' field to store comma-separated JE names.
            if created_journal_entries:
                pass
                # Assuming 'custom_linked_journal_entries' is a 'Data' field on Payroll Entry
                
                # self.db_set("custom_linked_journal_entries", ", ".join(created_journal_entries))
                
                # If it's a Table field, you'd do:
                # self.set("custom_je_links", [])
                # for je_name in created_journal_entries:
                #     self.append("custom_je_links", {"journal_entry": je_name})
                # self.save() # If self is not already saved in the calling context

            frappe.msgprint(_("Successfully created {0} Journal Entries for Payroll Entry {1}.").format(
                len(created_journal_entries), self.name))
            
            return created_journal_entries # Return the list of created JE names

        # else:
        #     # If not employee-based, create a single JE as before
        #     # This 'else' block needs to be part of the overridden method
        #     accounts = [] # Re-initialize accounts for this branch
            
        #     exchange_rate_credit, amount_credit = self.get_amount_and_exchange_rate_for_journal_entry(
        #         self.payment_account, total_je_payment_amount, company_currency, currencies
        #     )
        #     accounts.append(
        #         self.update_accounting_dimensions(
        #             {
        #                 "account": self.payment_account,
        #                 "bank_account": self.bank_account,
        #                 "credit_in_account_currency": flt(amount_credit, precision),
        #                 "exchange_rate": flt(exchange_rate_credit),
        #                 "cost_center": self.cost_center,
        #             },
        #             accounting_dimensions,
        #         )
        #     )

        #     exchange_rate_debit, amount_debit = self.get_amount_and_exchange_rate_for_journal_entry(
        #         payroll_payable_account, total_je_payment_amount, company_currency, currencies
        #     )
        #     accounts.append(
        #         self.update_accounting_dimensions(
        #             {
        #                 "account": payroll_payable_account,
        #                 "debit_in_account_currency": flt(amount_debit, precision),
        #                 "exchange_rate": flt(exchange_rate_debit),
        #                 "reference_type": self.doctype,
        #                 "reference_name": self.name,
        #                 "cost_center": self.cost_center,
        #             },
        #             accounting_dimensions,
        #         )
        #     )
            
        #     final_user_remark = _("Payment of !!!!!!!!!!!!!!!!!!!!!!!!!! {0} from {1} to {2}").format(
        #         _(user_remark), self.start_date, self.end_date
        #     )

        #     # This will create and return a single Journal Entry
        #     single_je_name = self.make_journal_entry(
        #         accounts,
        #         currencies,
        #         voucher_type="Bank Entry",
        #         user_remark=final_user_remark,
            # )
            # return [single_je_name] # Return as a list for consistency

    def make_journal_entry_with_party(
        self,
        accounts,
        currencies,
        payroll_payable_account=None,
        voucher_type="Journal Entry",
        user_remark="",
        submitted_salary_slips: list | None = None,
        submit_journal_entry=False,
    ) -> str:
        multi_currency = 0
        if len(currencies) > 1:
            multi_currency = 1

        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.voucher_type = voucher_type
        journal_entry.user_remark = user_remark
        journal_entry.company = self.company
        journal_entry.posting_date = self.posting_date

        # Add party type and party name from salary components
        for account in accounts:
            if "salary_component" in account:
                salary_component = account["salary_component"]
                party_type, party = frappe.db.get_value(
                    "Salary Component", salary_component, ["custom_party_type", "custom_party"]
                )
                if party_type and party:
                    account["party_type"] = party_type
                    account["party"] = party

        journal_entry.set("accounts", accounts)
        journal_entry.multi_currency = multi_currency

        if voucher_type == "Journal Entry":
            journal_entry.title = payroll_payable_account

        journal_entry.save(ignore_permissions=True)

        try:
            if submit_journal_entry:
                journal_entry.submit()

            if submitted_salary_slips:
                self.set_journal_entry_in_salary_slips(submitted_salary_slips, jv_name=journal_entry.name)

        except Exception as e:
            if type(e) in (str, list, tuple):
                frappe.msgprint(e)

            self.log_error("Journal Entry creation against Salary Slip failed")
            raise

        return journal_entry
    
    def get_salary_component_total_(
        self,
        component_type=None,
        process_payroll_accounting_entry_based_on_employee=False,
    ):
        print(";;;;;;;;;;;;;;;;;;;;;;;")
        salary_components = self.get_salary_components_(component_type)
        if salary_components:
            component_dict = {}

            for item in salary_components:
                if not self.should_add_component_to_accrual_jv(component_type, item):
                    continue

                employee_cost_centers = self.get_payroll_cost_centers_for_employee(
                    item.employee, item.salary_structure
                )
                employee_advance = self.get_advance_deduction(component_type, item)

                for cost_center, percentage in employee_cost_centers.items():
                    amount_against_cost_center = flt(item.amount) * percentage / 100

                    if employee_advance:
                        self.add_advance_deduction_entry(
                            item, amount_against_cost_center, cost_center, employee_advance
                        )
                    else:
                        key = (item.salary_component, cost_center)
                        component_dict[key] = component_dict.get(key, 0) + amount_against_cost_center

                    if process_payroll_accounting_entry_based_on_employee:
                        self.set_employee_based_payroll_payable_entries(
                            component_type, item.employee, amount_against_cost_center
                        )

            account_details = self.get_account(component_dict=component_dict)

            return account_details
        
    def get_account(self, component_dict=None):
            account_dict = {}
            for key, amount in component_dict.items():
                # key is (component, cost_center) from get_salary_component_total
                component, cost_center = key

                # Assuming this new method returns (account, party_type, party)
                account, party_type, party = get_salary_component_account_details(self , component)

                # The new accounting key includes account, cost_center, party_type, and party
                accounting_key = (account, cost_center, party_type, party)

                account_dict[accounting_key] = account_dict.get(accounting_key, 0) + amount

            return account_dict

    
    def get_salary_components_(self, component_type):
        salary_slips = self.get_sal_slip_list(ss_status=1, as_dict=True)

        if salary_slips:
            ss = frappe.qb.DocType("Salary Slip")
            sc = frappe.qb.DocType("Salary Component")
            ssd = frappe.qb.DocType("Salary Detail")
            salary_components = (
                frappe.qb.from_(ss)
                .join(ssd)
                .on(ss.name == ssd.parent)
                .join(sc)
                .on(ssd.salary_component == sc.name)
                .select(
                    ssd.salary_component,
                    ssd.amount,
                    ssd.parentfield,
                    ssd.additional_salary,
                    ss.salary_structure,
                    ss.employee,
                    sc.statistical_component,
                    sc.do_not_include_in_total,
                )

                .where(
                    (ssd.parentfield == component_type)
                    & (ss.name.isin(tuple([d.name for d in salary_slips])))
                    & (sc.statistical_component == 0)
                    & (sc.do_not_include_in_total == 0)
                )
            ).run(as_dict=True)

            return salary_components

    def get_sal_slip_list(self, ss_status, as_dict=False):
        """
        Returns list of salary slips based on selected criteria
        """
        print("KKKKKKKKKKKKKKKKKKKKKKKKK \n kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        ss = frappe.qb.DocType("Salary Slip")
        ss_list = (
            frappe.qb.from_(ss)
            .select(ss.name, ss.salary_structure)
            .where(
                (ss.docstatus == ss_status)
                & (ss.payroll_entry == self.name)
                & ((ss.journal_entry.isnull()) | (ss.journal_entry == ""))
                & (Coalesce(ss.salary_slip_based_on_timesheet, 0) == self.salary_slip_based_on_timesheet)
            )
        ).run(as_dict=as_dict)

        return ss_list

    @frappe.whitelist()
    def make_payment_entry(self):
        print ("Making payment entry")
        self.check_permission("write")
        self.employee_based_payroll_payable_entries = {}
        process_payroll_accounting_entry_based_on_employee = frappe.db.get_single_value(
            "Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
        )


        salary_slip_name_list = frappe.db.sql(
            """ select t1.name from `tabSalary Slip` t1
            where t1.docstatus == 1 and t1.payroll_entry = %s
            """,
            (self.name),
            as_list=True,
        )
        print(salary_slip_name_list)

        if salary_slip_name_list and len(salary_slip_name_list) > 0:
            salary_slip_total = 0
            for salary_slip_name in salary_slip_name_list:
                salary_slip = frappe.get_doc("Salary Slip", salary_slip_name[0])

                for sal_detail in salary_slip.earnings:
                    (
                        is_flexible_benefit,
                        only_tax_impact,
                        creat_separate_je,
                        statistical_component,
                        do_not_include_in_total,
                    ) = frappe.db.get_value(
                        "Salary Component",
                        sal_detail.salary_component,
                        [
                            "is_flexible_benefit",
                            "only_tax_impact",
                            "create_separate_payment_entry_against_benefit_claim",
                            "statistical_component",
                            "do_not_include_in_total",
                        ],
                    )
                    if only_tax_impact != 1 and statistical_component != 1 and do_not_include_in_total != 1:
                        if is_flexible_benefit == 1 and creat_separate_je == 1:
                            self.create_journal_entry(sal_detail.amount, sal_detail.salary_component)
                        else:
                            if process_payroll_accounting_entry_based_on_employee:
                                self.set_employee_based_payroll_payable_entries(
                                    "earnings",
                                    salary_slip.employee,
                                    sal_detail.amount,
                                    salary_slip.salary_structure,
                                )
                            salary_slip_total += sal_detail.amount

                for sal_detail in salary_slip.deductions:
                    (statistical_component,
                    do_not_include_in_total )= frappe.db.get_value(
                        "Salary Component", sal_detail.salary_component, ["statistical_component" , "do_not_include_in_total"],
                    )
                    if statistical_component != 1 and do_not_include_in_total != 1:
                        if process_payroll_accounting_entry_based_on_employee:
                            self.set_employee_based_payroll_payable_entries(
                                "deductions",
                                salary_slip.employee,
                                sal_detail.amount,
                                salary_slip.salary_structure,
                            )
                            print(sal_detail.salary_component)
                            print(sal_detail.salary_component)
                            print(sal_detail.salary_component)
                            print(sal_detail.salary_component)

                        salary_slip_total -= sal_detail.amount



            if salary_slip_total > 0:
                self.create_journal_entry(salary_slip_total, "salary")


    def make_journal_entry(
        self,
        accounts,
        currencies,
        payroll_payable_account=None,
        voucher_type="Journal Entry",
        user_remark="",
        submitted_salary_slips: list | None = None,
        submit_journal_entry=False,
    ) -> str:
        multi_currency = 0
        if len(currencies) > 1:
            multi_currency = 1

        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.voucher_type = voucher_type
        journal_entry.user_remark = user_remark
        journal_entry.company = self.company
        journal_entry.posting_date = self.posting_date

        journal_entry.set("accounts", accounts)
        journal_entry.multi_currency = multi_currency

        if voucher_type == "Journal Entry":
            journal_entry.title = payroll_payable_account

        journal_entry.save(ignore_permissions=True)

        try:
            if submit_journal_entry:
                journal_entry.submit()

            if submitted_salary_slips:
                self.set_journal_entry_in_salary_slips(submitted_salary_slips, jv_name=journal_entry.name)

        except Exception as e:
            if type(e) in (str, list, tuple):
                frappe.msgprint(e)

            self.log_error("Journal Entry creation against Salary Slip failed")
            raise

        return journal_entry

    @frappe.whitelist()
    def submit_salary_slips(self):
        self.check_permission("write")
        salary_slips = self.get_sal_slip_list(ss_status=0)
        if len(salary_slips) > 30 or frappe.flags.enqueue_payroll_entry:
            self.db_set("status", "Queued")
            frappe.enqueue(
                submit_salary_slips_for_employees_,
                timeout=600,
                payroll_entry=self,
                salary_slips=salary_slips,
                publish_progress=False,
            )
            frappe.msgprint(
                _("Salary Slip submission is queued. It may take a few minutes"),
                alert=True,
                indicator="blue",
            )
        else:
            submit_salary_slips_for_employees(self, salary_slips, publish_progress=False)



def submit_salary_slips_for_employees_(payroll_entry, salary_slips, publish_progress=True):
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    from hrms.payroll.doctype.payroll_entry.payroll_entry import show_payroll_submission_status ,log_payroll_failure

    try:
        submitted = []
        unsubmitted = []
        frappe.flags.via_payroll_entry = True
        count = 0

        for entry in salary_slips:
            salary_slip = frappe.get_doc("Salary Slip", entry[0])
            if salary_slip.net_pay < 0:
                unsubmitted.append(entry[0])
            else:
                try:
                    salary_slip.submit()
                    submitted.append(salary_slip)
                except frappe.ValidationError:
                    unsubmitted.append(entry[0])

            count += 1
            if publish_progress:
                frappe.publish_progress(
                    count * 100 / len(salary_slips), title=_("Submitting Salary Slips...")
                )

        if submitted:
            make_accrual_jv_entry(payroll_entry , submitted)
            payroll_entry.email_salary_slip(submitted)
            payroll_entry.db_set({"salary_slips_submitted": 1, "status": "Submitted", "error_message": ""})

        show_payroll_submission_status(submitted, unsubmitted, payroll_entry)

    except Exception as e:
        frappe.db.rollback()
        log_payroll_failure("submission", payroll_entry, e)

    finally:
        frappe.db.commit()  # nosemgrep
        frappe.publish_realtime("completed_salary_slip_submission")

    frappe.flags.via_payroll_entry = False




def make_accrual_jv_entry(self, submitted_salary_slips):
    self.check_permission("write")
    process_payroll_accounting_entry_based_on_employee = frappe.db.get_single_value(
        "Payroll Settings", "process_payroll_accounting_entry_based_on_employee"
    )

    self.employee_based_payroll_payable_entries = {}
    self._advance_deduction_entries = []

    earnings = (
        self.get_salary_component_total_(
            component_type="earnings",
            process_payroll_accounting_entry_based_on_employee=process_payroll_accounting_entry_based_on_employee,
        )
        or {}
    )

    deductions = (
        self.get_salary_component_total_(
            component_type="deductions",
            process_payroll_accounting_entry_based_on_employee=process_payroll_accounting_entry_based_on_employee,
        )
        or {}
    )

    precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

    if earnings or deductions:
        accounts = []
        currencies = []
        payable_amount = 0
        accounting_dimensions = get_accounting_dimensions() or []
        company_currency = erpnext.get_company_currency(self.company)

        payable_amount = get_payable_amount_for_earnings_and_deductions(
            self,
            accounts,
            earnings,
            deductions,
            currencies,
            company_currency,
            accounting_dimensions,
            precision,
            payable_amount,
        )

        payable_amount = self.set_accounting_entries_for_advance_deductions(
            accounts,
            currencies,
            company_currency,
            accounting_dimensions,
            precision,
            payable_amount,
        )

        self.set_payable_amount_against_payroll_payable_account(
            accounts,
            currencies,
            company_currency,
            accounting_dimensions,
            precision,
            payable_amount,
            self.payroll_payable_account,
            process_payroll_accounting_entry_based_on_employee,
        )

        self.make_journal_entry(
            accounts,
            currencies,
            self.payroll_payable_account,
            voucher_type="Journal Entry",
            user_remark=_("Accrual Journal Entry for salaries from {0} to {1}").format(
                self.start_date, self.end_date
            ),
            submit_journal_entry=True,
            submitted_salary_slips=submitted_salary_slips,
        )

# def get_payable_amount_for_earnings_and_deductions(
#     self,
#     accounts,
#     earnings,
#     deductions,
#     currencies,
#     company_currency,
#     accounting_dimensions,
#     precision,
#     payable_amount,
# ):
#     # Earnings
#     for acc_cc, amount , party  in earnings.items():
#         payable_amount = self.get_accounting_entries_and_payable_amount(
#             acc_cc[0],
#             acc_cc[1] or self.cost_center,
#             amount,
#             currencies,
#             company_currency,
#             payable_amount,
#             accounting_dimensions,
#             precision,
#             entry_type="debit",
#             party=party,
#             accounts=accounts,
#         )

#     # Deductions
#     for acc_cc, amount in deductions.items():
#         payable_amount = self.get_accounting_entries_and_payable_amount(
#             acc_cc[0],
#             acc_cc[1] or self.cost_center,
#             amount,
#             currencies,
#             company_currency,
#             payable_amount,
#             accounting_dimensions,
#             precision,
#             entry_type="credit",
#             accounts=accounts,
#         )

#     return payable_amount

def get_payable_amount_for_earnings_and_deductions(
    self,
    accounts,
    earnings,
    deductions,
    currencies,
    company_currency,
    accounting_dimensions,
    precision,
    payable_amount,
):
    # Earnings
    # Key is (account, cost_center, party_type, party), Value is amount
    for key, amount in earnings.items():
        # Correctly unpack the 4 elements from the key tuple
        account, cost_center, party_type, party = key

        # Pass the correct elements to the helper function
        payable_amount = get_accounting_entries_and_payable_amount_(
            self,
            account, # acc_cc[0] is now just 'account'
            cost_center or self.cost_center, # acc_cc[1] is now 'cost_center'
            amount,
            currencies,
            company_currency,
            payable_amount,
            accounting_dimensions,
            precision,
            entry_type="debit",
            party_type =party_type,
            party=party, # Pass party
            accounts=accounts,
        )

    # Deductions
    # The deductions dictionary keys should also be 4 elements now
    for key, amount in deductions.items():
        # Correctly unpack the 4 elements from the key tuple
        account, cost_center, party_type, party = key

        payable_amount = get_accounting_entries_and_payable_amount_(
            self,
            account, # acc_cc[0] is now 'account'
            cost_center or self.cost_center, # acc_cc[1] is now 'cost_center'
            amount,
            currencies,
            company_currency,
            payable_amount,
            accounting_dimensions,
            precision,
            entry_type="credit",
            party_type=party_type,
            party=party, # Pass party
            accounts=accounts,
        )

    return payable_amount

def get_accounting_entries_and_payable_amount_(
    self,
    account,
    cost_center,
    amount,
    currencies,
    company_currency,
    payable_amount,
    accounting_dimensions,
    precision,
    entry_type="credit",
    party_type=None,
    party=None,
    accounts=None,
    reference_type=None,
    reference_name=None,
    is_advance=None,
):
    exchange_rate, amt = self.get_amount_and_exchange_rate_for_journal_entry(
        account, amount, company_currency, currencies
    )

    row = {
        "account": account,
        "exchange_rate": flt(exchange_rate),
        "cost_center": cost_center,
        "project": self.project,
    }

    if entry_type == "debit":
        payable_amount += flt(amount, precision)
        row.update(
            {
                "debit_in_account_currency": flt(amt, precision),
            }
        )
    elif entry_type == "credit":
        payable_amount -= flt(amount, precision)
        row.update(
            {
                "credit_in_account_currency": flt(amt, precision),
            }
        )
    else:
        row.update(
            {
                "credit_in_account_currency": flt(amt, precision),
                "reference_type": self.doctype,
                "reference_name": self.name,
            }
        )

    if party and party_type:
        row.update(
            {
                "party_type": party_type,
                "party": party,
            }
        )

    if reference_type:
        row.update(
            {
                "reference_type": reference_type,
                "reference_name": reference_name,
                "is_advance": is_advance,
            }
        )

    self.update_accounting_dimensions(
        row,
        accounting_dimensions,
    )

    if amt:
        accounts.append(row)

    return payable_amount


# overried for the party on the salary componenet account table
def get_salary_component_account_details(self, salary_component):

    account = frappe.db.get_value(
			"Salary Component Account",
			{"parent": salary_component, "company": self.company},
			"account",
			cache=True,
		)

    custom_party_type = frappe.db.get_value(
                "Salary Component Account",
                {"parent": salary_component, "company": self.company},
                "custom_party_type",
                cache=True,
            )

    custom_party = frappe.db.get_value(
                "Salary Component Account",
                {"parent": salary_component, "company": self.company},
                "custom_party",
                cache=True,
            )


    if not account:
        frappe.throw(
            _("Please set account in Salary Component {0}").format(
                get_link_to_form("Salary Component", salary_component)
            )
        )

    return account ,custom_party_type, custom_party