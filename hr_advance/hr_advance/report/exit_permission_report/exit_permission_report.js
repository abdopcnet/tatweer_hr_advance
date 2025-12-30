// Copyright (c) 2025, Hadeel Milad and contributors
// For license information, please see license.txt



frappe.query_reports["Exit Permission Report"] = {
	"filters": [
		{
			label: __("Employee"),
			fieldname: "employee",
			fieldtype: "Link",
			options: "Employee",
		},

		{
			label: __("Department"),
			fieldname: "department",
			fieldtype: "Link",
			options: "Department",
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: [
				{ "value": "", "label": __("") },
				{ "value": "Open", "label": __("Open") },
				{ "value": "Approved", "label": __("Approved") },
				{ "value": "Rejected", "label": __("Rejected") },
				{ "value": "Cancelled", "label": __("Cancelled") },
			],
			// default: "Unpaid",	
		},
		{
			label: __("Type"),
			fieldname: "type",
			fieldtype: "Select",
			options: [
				{ "value": "", "label": __("") },
				{ "value": "ظرف شخصي", "label": __("ظرف شخصي") },
				{ "value": "مهمة عمل", "label": __("مهمة عمل") },
			],
			// default: "Unpaid",	
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start()

		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end()

		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"hidden": 1
		},
	]
};
