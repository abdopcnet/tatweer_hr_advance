frappe.ui.form.on("Employee", "onload", function(frm){
    frm.set_query("custom_employee_bank_branch", function(){
        return {
            query: "hr_advance.api.fetch_bank_branch_list",
            filters: {
              bank_name: frm.doc.custom_bank_name,
            },
          };
    });

});    
  
// frappe.ui.form.on('Employee', {
//   // frm passed as the first parameter
//   setup(frm) {
//       frm.doc.employee_number = 88888888888
//       frm.refresh_fields();
//   },

// })
