// Copyright (c) 2025, Hadeel Milad and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Leave allocation', {
	refresh: function (frm) {
		// Update required property for new_leaves_allocated based on yearly_leave_type
		if (frm.fields_dict.bulk_leave_allocation_table) {
			frm.fields_dict.bulk_leave_allocation_table.grid.update_docfield_property(
				'new_leaves_allocated',
				'reqd',
				cint(frm.doc.yearly_leave_type) === 0 ? 1 : 0,
			);
		}

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
					yearly_leave_type: cint(frm.doc.yearly_leave_type) || 0,
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
							row.carry_forward =
								employee.carry_forward !== undefined
									? employee.carry_forward
									: cint(frm.doc.yearly_leave_type) === 1
									? 1
									: 0;
							row.total_leaves_allocated = employee.total_leaves_allocated || 0;

							// Always set new_leaves_allocated to 0 (user can enter manually if needed)
							row.new_leaves_allocated = 0;
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
									let title = __('Success');
									let indicator = 'green';
									let message = '';

									// Show success count
									if (r.message.success_count > 0) {
										message = __('تم إنشاء {0} تخصيص إجازة.', [
											r.message.success_count || 0,
										]);
									}

									// Show failed allocations if any
									if (r.message.failed && r.message.failed.length > 0) {
										if (r.message.success_count > 0) {
											title = __('نجح جزئياً');
											indicator = 'orange';
										} else {
											title = __('فشل');
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
											__('فشل إنشاء {0} تخصيص إجازة:', [
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
												(item.error || __('خطأ غير معروف')) +
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

	yearly_leave_type: function (frm) {
		// When yearly_leave_type changes, update all rows in child table
		if (
			frm.doc.bulk_leave_allocation_table &&
			frm.doc.bulk_leave_allocation_table.length > 0
		) {
			frm.doc.bulk_leave_allocation_table.forEach(function (row) {
				// Keep existing new_leaves_allocated value (user can enter manually)
				// Don't copy from total_leaves_allocated
			});
			frm.refresh_field('bulk_leave_allocation_table');
		}

		// Update required property for new_leaves_allocated in child table
		frm.fields_dict.bulk_leave_allocation_table.grid.update_docfield_property(
			'new_leaves_allocated',
			'reqd',
			cint(frm.doc.yearly_leave_type) === 0 ? 1 : 0,
		);
	},
});

// Handle child table changes
frappe.ui.form.on('Bulk Leave allocation Table', {
	// Removed total_leaves_allocated handler - new_leaves_allocated should not copy from total_leaves_allocated

	carry_forward: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If carry_forward = 1, copy new_leaves_allocated to total_leaves_allocated
		if (cint(row.carry_forward) === 1 && row.new_leaves_allocated) {
			// Calculate total: unused_leaves + new_leaves_allocated
			// For now, just set total = new_leaves_allocated (will be recalculated on server)
			frappe.model.set_value(
				cdt,
				cdn,
				'total_leaves_allocated',
				row.new_leaves_allocated || 0,
			);
		}
	},

	new_leaves_allocated: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		// If carry_forward = 1, update total_leaves_allocated
		if (cint(row.carry_forward) === 1) {
			// Calculate total: unused_leaves + new_leaves_allocated
			// For now, just set total = new_leaves_allocated (will be recalculated on server)
			frappe.model.set_value(
				cdt,
				cdn,
				'total_leaves_allocated',
				row.new_leaves_allocated || 0,
			);
		}
	},
});
