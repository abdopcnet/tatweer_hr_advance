// Copyright (c) 2025, Hadeel Milad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Exit Permission Request", {
	// refresh(frm) {

	// },
    // validate: function(frm) {
    //     if (frm.doc.from_time && frm.doc.to_time) {
    //         const start = moment(frm.doc.from_time, 'HH:mm:ss');
    //         const end = moment(frm.doc.to_time, 'HH:mm:ss');

    //         if (start.isSameOrAfter(end)) {
    //             frappe.throw(__('Start Time must be less than End Time'));
    //         }
    //     }
    // }

    validate: function(frm) {
        if (frm.doc.from_time && frm.doc.to_time) {
            const start = moment(frm.doc.from_time, 'HH:mm:ss');
            const end = moment(frm.doc.to_time, 'HH:mm:ss');

            if (start.isSameOrAfter(end)) {
                frappe.throw(__('Start Time must be less than End Time'));
            }

            // Calculate duration in hours and minutes
            const duration = moment.duration(end.diff(start));
            const hours = duration.asHours().toFixed(2);  // Example: 2.50 hours

            frm.set_value('total_hours', hours);
            frm.refresh_fields();
        }
    },
    
});
