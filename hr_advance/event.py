import re
import frappe
from datetime import date
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, today
from frappe.utils.data import money_in_words
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import get_first_day_of_week, get_quarter_start, getdate , get_quarter_ending
from frappe.utils import add_days, cint, date_diff, flt, get_datetime, getdate, nowdate

import erpnext
import json

from dateutil.relativedelta import relativedelta



@frappe.whitelist()
def summation_task_cost(doc, method):
    # frappe.throw("The total Tasks Cost for the Linked Project is greater then the Estimated Costing for the project")

    if (doc.custom_task):
        main_task = frappe.get_doc("Task" , doc.custom_task)
        total_purchase_invoice_linked = frappe.db.get_all("Purchase Invoice" , filters={"docstatus" : ['!=' , 2] , 'custom_task' : ['=' , main_task.name]})
        task_cost = 0
        # custom_total_expense_cost = 00
        for PI in total_purchase_invoice_linked:
            task_cost = task_cost + frappe.db.get_value("Purchase Invoice" , PI.name ,'grand_total' )
        total_project_task_cost = 0
        project_tasks = frappe.db.get_all("Task" , filters={"Project" :['=' ,  doc.project]})
        for task in project_tasks:
            total_project_task_cost = total_project_task_cost + frappe.db.get_value("Task" , task.name ,'custom_total_expense_cost' )
        estimated_costing =  frappe.db.get_value("Project" , main_task.project ,'estimated_costing' )
        if total_project_task_cost > estimated_costing:
            frappe.throw("The total Tasks Cost for the Linked Project is greater then the Estimated Costing for the project")

        frappe.db.set_value('Task' , doc.custom_task , 'custom_total_expense_cost' , task_cost)
        # frappe.db.set_value('Task' , doc.name , 'custom_total_expense_cost' , 900)
        # doc.custom_total_expense_cost =  8000
        # doc.save()
        frappe.db.commit()





@frappe.whitelist()
def cancel_task_cost(doc, method):
    # frappe.throw("The total Tasks Cost for the Linked Project is greater then the Estimated Costing for the project")

    if (doc.custom_task):
        main_task = frappe.get_doc("Task" , doc.custom_task)
        total_purchase_invoice_linked = frappe.db.get_all("Purchase Invoice" , filters={"docstatus" : ['!=' , 2] , 'custom_task' : ['=' , main_task.name]})
        task_cost = 0
        # custom_total_expense_cost = 00
        for PI in total_purchase_invoice_linked:
            task_cost = task_cost + frappe.db.get_value("Purchase Invoice" , PI.name ,'grand_total' )
        total_project_task_cost = -1 * doc.grand_total
        project_tasks = frappe.db.get_all("Task" , filters={"Project" :['=' ,  doc.project]})
        for task in project_tasks:
            total_project_task_cost = total_project_task_cost + frappe.db.get_value("Task" , task.name ,'custom_total_expense_cost' )
        estimated_costing =  frappe.db.get_value("Project" , main_task.project ,'estimated_costing' )
        # if total_project_task_cost > estimated_costing:
        #     frappe.throw("The total Tasks Cost for the Linked Project is greater then the Estimated Costing for the project")

        frappe.db.set_value('Task' , doc.custom_task , 'custom_total_expense_cost' , task_cost)
        # frappe.db.set_value('Task' , doc.name , 'custom_total_expense_cost' , 900)
        # doc.custom_total_expense_cost =  8000
        # doc.save()
        frappe.db.commit()


def validate_leave_no_earlier_submission_allowed(doc, method):
    if doc.leave_type:
        # frappe.throw("hi")
        no_earlier_submission_allowed = frappe.db.get_value("Leave Type" , doc.leave_type  , "custom_no_earlier_submission_allowed")
        if no_earlier_submission_allowed:
            from_date_obj = get_datetime(doc.from_date).date()
            to_date_obj = get_datetime(doc.to_date).date()
            today_date_obj = get_datetime(today()).date()

            # If the leave starts *after* today, throw an error.
            if from_date_obj >= today_date_obj:
                frappe.throw("Cannot apply for this leave type for a future date.")
            # If the leave end *after* today, throw an error.
            if to_date_obj >= today_date_obj:
                frappe.throw("Cannot apply for this leave type for a future date.")