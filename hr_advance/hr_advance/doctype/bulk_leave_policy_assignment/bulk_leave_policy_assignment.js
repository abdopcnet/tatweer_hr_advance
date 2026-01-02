// Copyright (c) 2026, Hadeel Milad and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Leave Policy Assignment', {
	refresh: function (frm) {
		// Get Active Employees button
		frm.add_custom_button(__('👥 Get Active Employees'), function () {
			if (!frm.doc.company) {
				frappe.msgprint(__('Please select Company first'));
				return;
			}
			if (!frm.doc.leave_policy) {
				frappe.msgprint(__('Please select Leave Policy first'));
				return;
			}
			if (!frm.doc.effective_from) {
				frappe.msgprint(__('Please select Effective From date first'));
				return;
			}
			if (!frm.doc.effective_to) {
				frappe.msgprint(__('Please select Effective To date first'));
				return;
			}

			frappe.call({
				method: 'hr_advance.hr_advance.doctype.bulk_leave_policy_assignment.bulk_leave_policy_assignment.get_active_employees',
				args: {
					company: frm.doc.company,
					leave_policy: frm.doc.leave_policy,
					assignment_based_on: frm.doc.assignment_based_on || '',
					effective_from: frm.doc.effective_from,
					effective_to: frm.doc.effective_to,
					leave_period: frm.doc.leave_period || null,
					department: frm.doc.department || null,
				},
				freeze: true,
				freeze_message: __('Fetching active employees...'),
				callback: function (r) {
					if (!r.exc && r.message) {
						// Clear existing rows
						frm.clear_table('bulk_leave_policy_assignment_table');

						// Add employees to child table
						r.message.forEach(function (employee) {
							let row = frm.add_child('bulk_leave_policy_assignment_table');
							row.employee = employee.employee;
							row.employee_name = employee.employee_name;
							row.department = employee.department || '';
							row.company = employee.company || '';
							row.status = employee.has_existing_assignment ? __('Existing Assignment') : __('Pending');
						});

						frm.refresh_field('bulk_leave_policy_assignment_table');
						frappe.msgprint({
							message: __('{0} employees added to the table', [r.message.length]),
							indicator: 'green',
							alert: true,
						});
					}
				},
			});
		});

		// Create Bulk Leave Policy Assignments button - only show if there are rows
		if (
			frm.doc.bulk_leave_policy_assignment_table &&
			frm.doc.bulk_leave_policy_assignment_table.length > 0
		) {
			frm.add_custom_button(__('Create Bulk Leave Policy Assignments'), function () {
				if (!frm.doc.company) {
					frappe.msgprint(__('Please select Company first'));
					return;
				}
				if (!frm.doc.leave_policy) {
					frappe.msgprint(__('Please select Leave Policy first'));
					return;
				}
				if (frm.doc.bulk_leave_policy_assignment_table.length === 0) {
					frappe.msgprint(__('Please add employees to the table first'));
					return;
				}

				frappe.confirm(
					__('Are you sure you want to create {0} Leave Policy Assignment documents?', [
						frm.doc.bulk_leave_policy_assignment_table.length,
					]),
					function () {
						// Yes
						frappe.call({
							method: 'hr_advance.hr_advance.doctype.bulk_leave_policy_assignment.bulk_leave_policy_assignment.create_bulk_leave_policy_assignments',
							args: {
								bulk_assignment_name: frm.doc.name,
							},
							freeze: true,
							freeze_message: __('Creating Leave Policy Assignments...'),
							callback: function (r) {
								if (!r.exc && r.message) {
									let title = __('Success');
									let indicator = 'green';
									let message = '';

									// Show success count
									if (r.message.success_count > 0) {
										message = __('{0} Leave Policy Assignments created successfully.', [
											r.message.success_count || 0,
										]);
									}

									// Show failed assignments if any
									if (r.message.failed && r.message.failed.length > 0) {
										if (r.message.success_count > 0) {
											title = __('Partial Success');
											indicator = 'orange';
										} else {
											title = __('Failed');
											indicator = 'red';
										}

										// Build message with better formatting
										let fullMessage = '';
										if (message) {
											fullMessage =
												'<div style="margin-bottom: 15px;">' +
												message +
												'</div>';
										}
										fullMessage +=
											'<div style="margin-bottom: 10px; font-weight: bold;">' +
											__('Failed to create {0} assignments:', [
												r.message.failed_count || 0,
											]) +
											'</div>';

										// Create styled list for errors
										fullMessage += '<div style="margin-top: 10px;">';
										r.message.failed.forEach(function (item) {
											fullMessage +=
												'<div style="margin-bottom: 10px; padding: 8px; background-color: #fff3cd; border-right: 3px solid #ffc107; border-radius: 3px;">' +
												'<strong>' +
												(item.employee_name || item.employee) +
												':</strong><br>' +
												'<span style="color: #856404;">' +
												(item.error || __('Unknown error')) +
												'</span></div>';
										});
										fullMessage += '</div>';

										frappe.msgprint({
											title: title,
											message: fullMessage,
											indicator: indicator,
											is_minimizable: true,
											wide: true,
										});
									} else {
										// All succeeded
										frappe.msgprint({
											title: title,
											message: message,
											indicator: indicator,
											alert: true,
										});
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

	assignment_based_on: function (frm) {
		// Set effective dates based on assignment_based_on
		if (frm.doc.assignment_based_on == "Leave Period" && frm.doc.leave_period) {
			frappe.model.with_doc("Leave Period", frm.doc.leave_period, function () {
				let from_date = frappe.model.get_value(
					"Leave Period",
					frm.doc.leave_period,
					"from_date",
				);
				let to_date = frappe.model.get_value(
					"Leave Period",
					frm.doc.leave_period,
					"to_date",
				);
				frm.set_value("effective_from", from_date);
				frm.set_value("effective_to", to_date);
			});
		}
		frm.refresh();
	},

	leave_period: function (frm) {
		// Set effective dates when leave period is selected
		if (frm.doc.assignment_based_on == "Leave Period" && frm.doc.leave_period) {
			frappe.model.with_doc("Leave Period", frm.doc.leave_period, function () {
				let from_date = frappe.model.get_value(
					"Leave Period",
					frm.doc.leave_period,
					"from_date",
				);
				let to_date = frappe.model.get_value(
					"Leave Period",
					frm.doc.leave_period,
					"to_date",
				);
				frm.set_value("effective_from", from_date);
				frm.set_value("effective_to", to_date);
			});
		}
		frm.refresh();
	},
});

// Set query for leave_period
frappe.ui.form.on('Bulk Leave Policy Assignment', {
	setup: function (frm) {
		frm.set_query("leave_period", function () {
			return {
				filters: {
					is_active: 1,
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("leave_policy", function () {
			return {
				filters: {
					docstatus: 1,
				},
			};
		});
	},
});
