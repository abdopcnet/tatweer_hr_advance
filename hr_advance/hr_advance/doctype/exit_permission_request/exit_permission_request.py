# Copyright (c) 2025, Hadeel Milad and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate
import frappe


class ExitPermissionRequest(Document):
	
	def validate(self):
		current_month = getdate(nowdate()).strftime("%Y-%m")
		if self.type == 'ظرف شخصي':
			count = frappe.db.count(
				"Exit Permission Request",
				filters={
					"employee": self.employee,
					"docstatus": 1,
					"for_date": ["like", f"{current_month}%"],
					"type": 'ظرف شخصي',
				}
			)
			max_requests = frappe.db.get_single_value("HR Settings", "custom_max_exit_permission_request_per_month")
			
			if count >= max_requests:
				frappe.throw(f"Maximum exit permission requests for the month reached: {max_requests}")
			existing_request = frappe.db.exists(
				"Exit Permission Request",
				{
					"employee": self.employee,
					"for_date": self.for_date,
					"type": self.type,
					"docstatus": 1,
				},
			)
			if existing_request:
				frappe.msgprint("An exit permission request for the same employee, date, and type already exists.")