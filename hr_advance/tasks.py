
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
import json
from frappe.utils import (
    flt,
    getdate,
    nowdate,
)
from frappe.utils import cint, cstr, flt, today



@frappe.whitelist()
def calculate_exp_yrears_in_employee():
    frappe.db.sql(
         f"""
         UPDATE tabEmployee AS e
         SET
         e.custom_total_insed_experience_in_years =DATEDIFF(NOW(), e.date_of_joining)/365 
             WHERE e.status = "Active";
         """)
    frappe.db.sql(
            f"""
            UPDATE tabEmployee AS e
            SET
            e.custom_total_experience_in_years  = (DATEDIFF(NOW(), e.date_of_joining)/365 + e.custom_total_external_experians_year )
                WHERE e.status = "Active";
            """)
    frappe.db.commit()

@frappe.whitelist()
def update_supplier_status():
    supplier_expired_list = frappe.db.get_all("Supplier" , filters={"custom_license_expiration_date": ("<=", '19-07-2025'), "is_frozen" : 0 })
    print(supplier_expired_list)
    for suppliers in supplier_expired_list:
        supplier = frappe.get_doc("Supplier" , suppliers.name)
        if not supplier.custom_license_expiration_date:
            pass
        supplier.is_frozen = 1
        supplier.save()
        # frappe.db_set_value('Suppliers' , supplier.name ,"is_frozen" , 1 )
        comment = frappe.new_doc("Comment")
        comment.comment_type = "Comment" # Or "Correction", "Assigned", etc.
        comment.reference_doctype = "Supplier"
        comment.reference_name = supplier.name
        # comment.comment_email = comment_by if comment_by else frappe.session.user
        comment.content = (f"This Supplier was froze on the , becose the License Expiration Date on the {supplier.custom_license_expiration_date}")
        comment.save(ignore_permissions=True) # Use ignore_permissions if adding system comments
        frappe.db.commit()
