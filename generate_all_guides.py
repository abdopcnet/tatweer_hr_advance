#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate guide files for ALL DocTypes in hr_advance and hrms
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
	depends_on = field.get('depends_on', '')
	fetch_from = field.get('fetch_from', '')

	desc = f"- `{fieldname}` ({fieldtype}"
	if reqd:
		desc += ", Required"
	if read_only:
		desc += ", Read-only"
	if options and fieldtype in ['Link', 'Select']:
		desc += f", Options: {options}"
	if default and default != "Today":
		desc += f", Default: {default}"
	desc += f"): {label}"

	if fetch_from:
		desc += f" (Fetched from: {fetch_from})"
	if depends_on:
		desc += f" (Depends on: {depends_on})"

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

	# Skip child tables
	if doctype_data.get('istable', 0):
		return False

	fields = doctype_data.get('fields', [])
	field_order = doctype_data.get('field_order', [])
	is_submittable = doctype_data.get('is_submittable', 0)
	autoname = doctype_data.get('autoname', '')

	# Generate markdown content
	content = f"# {doctype_name}\n\n"
	content += "## Overview\n"
	content += f"{doctype_name} DocType for {app_name}.\n\n"

	# Fields section
	content += "## Fields\n\n"

	# Group fields by sections
	main_fields = []
	table_fields = []
	read_only_fields = []

	for field in fields:
		fieldname = field.get('fieldname', '')
		fieldtype = field.get('fieldtype', '')

		# Skip layout fields and system fields
		if fieldtype in ['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Button', 'Fold']:
			continue
		if fieldname in ['amended_from', 'owner', 'creation', 'modified', 'modified_by']:
			continue

		if fieldtype == 'Table':
			table_fields.append(field)
		elif field.get('read_only', 0):
			read_only_fields.append(field)
		else:
			main_fields.append(field)

	if main_fields:
		content += "### Main Fields\n\n"
		for field in main_fields[:15]:  # Limit to 15 fields
			content += get_field_description(field) + "\n"
		if len(main_fields) > 15:
			content += f"\n*... and {len(main_fields) - 15} more fields*\n"
		content += "\n"

	if read_only_fields:
		content += "### Read-only Fields\n\n"
		for field in read_only_fields[:10]:  # Limit to 10 fields
			content += get_field_description(field) + "\n"
		if len(read_only_fields) > 10:
			content += f"\n*... and {len(read_only_fields) - 10} more fields*\n"
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
		for field in required_fields[:8]:  # Limit to 8
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

	if autoname:
		content += f"\n### Naming\n"
		content += f"- Auto-naming: {autoname}\n"

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
	hr_advance_path = base_path / 'hr_advance' / 'hr_advance' / 'hr_advance' / 'doctype'
	output_base_hr_advance = base_path / 'hr_advance' / 'hr_advance_short_guide_files'

	hr_advance_doctypes = []
	for json_file in hr_advance_path.glob('**/*.json'):
		if '__pycache__' not in str(json_file) and 'test_records' not in str(json_file):
			doctype_name = json_file.parent.name
			hr_advance_doctypes.append((json_file, doctype_name))

	# Sort and number
	hr_advance_doctypes.sort(key=lambda x: x[1])

	print(f"Processing {len(hr_advance_doctypes)} hr_advance doctypes...")
	for idx, (json_path, doctype_name) in enumerate(hr_advance_doctypes, 1):
		output_file = output_base_hr_advance / f"{idx}.{doctype_name}.md"
		if generate_guide_from_json(json_path, output_file, 'HR Advance'):
			print(f"Generated: {output_file.name}")

	# Process ALL hrms/hr doctypes
	hrms_hr_path = base_path / 'hrms' / 'hrms' / 'hr' / 'doctype'
	output_base_hrms = base_path / 'hr_advance' / 'hrms_short_guide_files'

	hrms_doctypes = []
	for json_file in hrms_hr_path.glob('**/*.json'):
		if '__pycache__' not in str(json_file) and 'test_records' not in str(json_file):
			doctype_name = json_file.parent.name
			# Skip child tables that are already covered
			if doctype_name not in ['leave_policy_detail', 'leave_allocation_detail']:
				hrms_doctypes.append((json_file, doctype_name))

	# Sort and number
	hrms_doctypes.sort(key=lambda x: x[1])

	print(f"\nProcessing {len(hrms_doctypes)} hrms/hr doctypes...")
	for idx, (json_path, doctype_name) in enumerate(hrms_doctypes, 1):
		output_file = output_base_hrms / f"{idx}.{doctype_name}.md"
		if generate_guide_from_json(json_path, output_file, 'HRMS'):
			print(f"Generated: {output_file.name}")

	# Process ALL hrms/payroll doctypes
	hrms_payroll_path = base_path / 'hrms' / 'hrms' / 'payroll' / 'doctype'

	payroll_doctypes = []
	for json_file in hrms_payroll_path.glob('**/*.json'):
		if '__pycache__' not in str(json_file) and 'test_records' not in str(json_file):
			doctype_name = json_file.parent.name
			# Skip child tables
			if not doctype_name.endswith('_detail'):
				payroll_doctypes.append((json_file, doctype_name))

	# Sort and number
	payroll_doctypes.sort(key=lambda x: x[1])

	print(f"\nProcessing {len(payroll_doctypes)} hrms/payroll doctypes...")
	start_idx = len(hrms_doctypes) + 1
	for idx, (json_path, doctype_name) in enumerate(payroll_doctypes, 1):
		output_file = output_base_hrms / f"{start_idx + idx - 1}.{doctype_name}.md"
		if generate_guide_from_json(json_path, output_file, 'HRMS Payroll'):
			print(f"Generated: {output_file.name}")

	print("\nDone!")

if __name__ == '__main__':
	main()

