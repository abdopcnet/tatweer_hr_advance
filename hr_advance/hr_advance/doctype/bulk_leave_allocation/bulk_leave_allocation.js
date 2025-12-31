// Copyright (c) 2025, Hadeel Milad and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Leave allocation', {
	refresh: function (frm) {
		// Get Active Employees button with emoji
		frm.add_custom_button(__('👥 Get Active Employees'), function () {
			if (!frm.doc.company) {
				frappe.msgprint(__('Please select Company first'));
				return;
			}
			if (!frm.doc.leave_type) {
				frappe.msgprint(__('Please select Leave Type first'));
				return;
			}
			if (!frm.doc.from_date) {
				frappe.msgprint(__('Please select From Date first'));
				return;
			}
			if (!frm.doc.to_date) {
				frappe.msgprint(__('Please select To Date first'));
				return;
			}

			frappe.call({
				method: 'hr_advance.hr_advance.doctype.bulk_leave_allocation.bulk_leave_allocation.get_active_employees',
				args: {
					company: frm.doc.company,
					leave_type: frm.doc.leave_type,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
					department: frm.doc.department || null,
				},
				freeze: true,
				freeze_message: __('Fetching active employees...'),
				callback: function (r) {
					if (!r.exc && r.message) {
						// Clear existing rows
						frm.clear_table('bulk_leave_allocation_table');

						// Add employees to child table
						r.message.forEach(function (employee) {
							let row = frm.add_child('bulk_leave_allocation_table');
							row.employee = employee.employee;
							row.employee_name = employee.employee_name;
							row.department = employee.department || '';
							row.company = employee.company;
							row.leave_type = employee.leave_type;
							row.from_date = employee.from_date;
							row.to_date = employee.to_date;
							row.new_leaves_allocated = employee.new_leaves_allocated || 0;
							row.carry_forward = employee.carry_forward || 0;
							row.total_leaves_allocated = employee.total_leaves_allocated || 0;
						});

						frm.refresh_field('bulk_leave_allocation_table');
						frappe.msgprint({
							message: __('{0} employees added to the table', [r.message.length]),
							indicator: 'green',
							alert: true,
						});
					}
				},
			});
		});

		// Create Bulk Leave Allocations button - only show if there are rows
		if (
			frm.doc.bulk_leave_allocation_table &&
			frm.doc.bulk_leave_allocation_table.length > 0
		) {
			frm.add_custom_button(__('Create Bulk Leave Allocations'), function () {
				if (!frm.doc.company) {
					frappe.msgprint(__('Please select Company first'));
					return;
				}
				if (!frm.doc.leave_type) {
					frappe.msgprint(__('Please select Leave Type first'));
					return;
				}
				if (frm.doc.bulk_leave_allocation_table.length === 0) {
					frappe.msgprint(__('Please add employees to the table first'));
					return;
				}

				frappe.confirm(
					__('Are you sure you want to create {0} Leave Allocation documents?', [
						frm.doc.bulk_leave_allocation_table.length,
					]),
					function () {
						// Yes
						frappe.call({
							method: 'hr_advance.hr_advance.doctype.bulk_leave_allocation.bulk_leave_allocation.create_bulk_leave_allocations',
							args: {
								bulk_allocation_name: frm.doc.name,
							},
							freeze: true,
							freeze_message: __('Creating Leave Allocations...'),
							callback: function (r) {
								if (!r.exc && r.message) {
									frappe.msgprint({
										title: __('Success'),
										message: __(
											'Created {0} Leave Allocation documents. {1} failed.',
											[
												r.message.success_count || 0,
												r.message.failed_count || 0,
											],
										),
										indicator: 'green',
										alert: true,
									});
									if (r.message.failed && r.message.failed.length > 0) {
										console.log('Failed allocations:', r.message.failed);
									}
									// Reload the form
									frm.reload_doc();
								}
							},
						});
					},
					function () {
						// No
					},
				);
			});
		}
	},
});
