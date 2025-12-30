# Copyright (c) 2025, Hadeel Milad and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	conditions = get_conditions(filters)
	columns, data =  get_columns(), get_data(conditions , filters)
	chart = get_chart_data(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary

def get_columns():
	
    columns = [
        {
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
			"width": 100,

        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
			"width": 200,

        },
        {
            "label": _("Type"),
            "fieldname": "type",
            "fieldtype": "Data",
			"width": 100,

        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("For Date"),
            "fieldname": "for_date",
            "fieldtype": "Date",
        },
        {
            "label": _("From Time"),
            "fieldname": "from_time",
            "fieldtype": "Time",
        },
		{
            "label": _("To Time"),
            "fieldname": "to_time",
            "fieldtype": "Time",
        },
        {
            "label": _("Total Hours"),
            "fieldname": "total_hours",
            "fieldtype": "float",
        },
		
	]
    return columns

def get_data(conditions , filters):
    data = frappe.db.sql(
        f"""
		SELECT
            *
		FROM `tabExit Permission Request` 
			{conditions}""",
			filters,
			as_dict=True)
    
    return data

def get_conditions(filters):
    
	
	conditions = " WHERE docstatus=1"
	employee = filters.get("employee")
	department = filters.get("department") 
	status = filters.get("status")
		
	if employee:
		conditions += " AND employee = '{0}' ".format(employee)
	if department:
			conditions += " AND department = '{0}' ".format(department)
	if status:
			conditions += " AND status = '{0}' ".format(status)

	if filters.get("from_date"):
		conditions += (" AND for_date >= '{0}'".format(filters.get("from_date")))

	if filters.get("to_date"):
		conditions += (" AND for_date <= '{0}'".format(filters.get("to_date")))


	print(conditions)

	return conditions


def get_report_summary(data):
	if not data:
		return None

	work = personal   = total_hours = 0
	if not data:
		return None
	for entry in data:
		if entry.type == "مهمة عمل":
			work += 1
		elif entry.type == "ظرف شخصي":
			personal += 1


		if entry.total_hours:
			total_hours += entry.total_hours

	return [
		{
			"value": work,
			"indicator": "Green",
			"label": _("Work Records"),
			"datatype": "Int",
		},
		{
			"value": personal,
			"indicator": "Blue",
			"label": _("Personal Records"),
			"datatype": "Int",
		},
		{
			"value": total_hours,
			"indicator": "Red",
			"label": _("Total Exits Hours"),
			"datatype": "Float",
		},
	]


def get_chart_data(data):
	if not data:
		return None

	total_work = {}
	for entry in data:
		total_work.setdefault(entry.type, 0)
		total_work[entry.type] += 1

	labels = [_(d) for d in list(total_work)]
	chart = {
		"data": {
			"labels": labels,
			"datasets": [{"name": _("Type"), "values": list(total_work.values())}],
		},
		"type": "percentage",
	}
	return chart
