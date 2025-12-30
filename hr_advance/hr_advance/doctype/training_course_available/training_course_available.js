// Copyright (c) 2025, Hadeel Milad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Training Course Available", {
	refresh(frm) {
        frm.add_custom_button(__('Employee Training Request'), function() {

            const TR = frappe.model.get_new_doc('Employee Training Request');
				TR.training_course = frm.doc.name;
				TR.request_date = frappe.datetime.now_date();
				// TR.naming_series = "TR/SER/.FY./.####";
				frappe.set_route('Form', TR.doctype, TR.name);
                
    //         frappe.set_route("Form", "Employee Training Request", {
    //         "training_course": frm.doc.name, 
    //         // "received_item": frm.doc.item_name,
    // });
}
    
)
        
	},
});


