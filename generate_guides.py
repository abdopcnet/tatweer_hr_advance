#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate guide files for all DocTypes
"""
import json
import os
import re
from pathlib import Path


def get_field_description(field):
    """Generate field description from field definition"""
    fieldname = field.get('fieldname', '')
    fieldtype = field.get('fieldtype', '')
    label = field.get('label', fieldname)
    reqd = field.get('reqd', 0)
    read_only = field.get('read_only', 0)
    options = field.get('options', '')
    default = field.get('default', '')

    desc = f"- `{fieldname}` ({fieldtype}"
    if reqd:
        desc += ", Required"
    if read_only:
        desc += ", Read-only"
    if options:
        desc += f", Options: {options}"
    if default:
        desc += f", Default: {default}"
    desc += f"): {label}"

    return desc


def generate_guide_from_json(json_path, output_path, app_name):
    """Generate guide file from DocType JSON"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            doctype_data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return False

    doctype_name = doctype_data.get('name', '')
    if not doctype_name:
        return False

    # Skip child tables and system doctypes
    if doctype_data.get('istable', 0) or doctype_name.startswith('__'):
        return False

    fields = doctype_data.get('fields', [])
    field_order = doctype_data.get('field_order', [])
    is_submittable = doctype_data.get('is_submittable', 0)

    # Generate markdown content
    content = f"# {doctype_name}\n\n"
    content += "## Overview\n"
    content += f"{doctype_name} DocType for {app_name}.\n\n"

    # Fields section
    content += "## Fields\n\n"

    # Group fields by sections
    main_fields = []
    table_fields = []

    for field in fields:
        fieldname = field.get('fieldname', '')
        fieldtype = field.get('fieldtype', '')

        # Skip layout fields
        if fieldtype in ['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Button']:
            continue

        if fieldtype == 'Table':
            table_fields.append(field)
        else:
            main_fields.append(field)

    if main_fields:
        content += "### Main Fields\n\n"
        for field in main_fields:
            content += get_field_description(field) + "\n"
        content += "\n"

    if table_fields:
        content += "### Child Tables\n\n"
        for field in table_fields:
            fieldname = field.get('fieldname', '')
            label = field.get('label', fieldname)
            options = field.get('options', '')
            content += f"- `{fieldname}` (Table): {label}\n"
            if options:
                content += f"  - Options: {options}\n"
        content += "\n"

    # Workflow section
    content += "## Workflow\n\n"
    content += "### Step 1: Create Document\n"
    content += f"1. Go to {app_name} → {doctype_name} → New\n"

    required_fields = [f for f in main_fields if f.get('reqd', 0)]
    if required_fields:
        content += "2. Fill required fields:\n"
        for field in required_fields[:5]:  # Limit to 5
            fieldname = field.get('fieldname', '')
            label = field.get('label', fieldname)
            content += f"   - `{fieldname}`: {label}\n"

    content += "\n### Step 2: Save/Submit\n"
    if is_submittable:
        content += "1. Review all fields\n"
        content += "2. Save document\n"
        content += "3. Submit document\n"
    else:
        content += "1. Review all fields\n"
        content += "2. Save document\n"

    content += "\n## Important Notes\n"
    content += "- Document must be saved to be effective\n"
    if is_submittable:
        content += "- Document must be submitted to be effective\n"

    # Write file
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}")
        return False


def main():
    base_path = Path('/home/frappe/frappe-bench/apps')

    # Process hr_advance doctypes
    hr_advance_path = base_path / 'hr_advance' / \
        'hr_advance' / 'hr_advance' / 'doctype'
    output_base = base_path / 'hr_advance' / 'hr_advance_short_guide_files'

    hr_advance_doctypes = []
    for json_file in hr_advance_path.glob('**/*.json'):
        if '__pycache__' not in str(json_file):
            doctype_name = json_file.parent.name
            hr_advance_doctypes.append((json_file, doctype_name))

    # Sort and number
    hr_advance_doctypes.sort(key=lambda x: x[1])

    for idx, (json_path, doctype_name) in enumerate(hr_advance_doctypes, 1):
        output_file = output_base / f"{idx}.{doctype_name}.md"
        generate_guide_from_json(json_path, output_file, 'HR Advance')
        print(f"Generated: {output_file}")

    # Process hrms doctypes (main ones only)
    hrms_hr_path = base_path / 'hrms' / 'hrms' / 'hr' / 'doctype'
    hrms_payroll_path = base_path / 'hrms' / 'hrms' / 'payroll' / 'doctype'
    output_base_hrms = base_path / 'hr_advance' / 'hrms_short_guide_files'

    # Important hrms doctypes
    important_doctypes = [
        'employee', 'leave_allocation', 'leave_policy', 'leave_policy_assignment',
        'leave_application', 'leave_type', 'leave_period', 'attendance',
        'salary_structure', 'salary_structure_assignment', 'payroll_entry',
        'employee_onboarding', 'employee_separation', 'expense_claim'
    ]

    hrms_doctypes = []
    for doctype_name in important_doctypes:
        json_path = hrms_hr_path / doctype_name / f'{doctype_name}.json'
        if not json_path.exists():
            json_path = hrms_payroll_path / \
                doctype_name / f'{doctype_name}.json'
        if json_path.exists():
            hrms_doctypes.append((json_path, doctype_name))

    # Sort and number
    hrms_doctypes.sort(key=lambda x: x[1])

    for idx, (json_path, doctype_name) in enumerate(hrms_doctypes, 1):
        output_file = output_base_hrms / f"{idx}.{doctype_name}.md"
        generate_guide_from_json(json_path, output_file, 'HRMS')
        print(f"Generated: {output_file}")


if __name__ == '__main__':
    main()
