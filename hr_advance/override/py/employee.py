
from erpnext.setup.doctype.employee.employee import Employee
from erpnext.setup.doctype.employee.employee import set_name_by_naming_series

import frappe


class EmployeeOverride(Employee):
	def autoname(self):
		naming_method = frappe.db.get_value("HR Settings", None, "emp_created_by")
		if not naming_method:
			frappe.throw(_("Please setup Employee Naming System in Human Resource > HR Settings"))
		else:
			if naming_method == "Naming Series":
				set_name_by_naming_series(self)
			elif naming_method == "Employee Number":
				self.name = self.employee_number
			elif naming_method == "Full Name":
				self.set_employee_name()
				self.name = self.employee_name

		self.employee = self.name
	def set_employee_name(self):
		self.employee_name = " ".join(
			filter(lambda x: x, [self.first_name, self.middle_name , self.last_name ,  self.custom_title])
		)
	# def before_insert(self):
	# 	new_series =  self.employee_number
	# 	try:
	# 		if len(new_series) >= 4:
	# 			frappe.client.set_value("HR Settings", "HR Settings", "custom_last_employee_series", new_series[-4:])
	# 		else:
	# 			print ("HR Setting upload error")
	# 			return ""
	# 	except IndexError:
	# 		pass