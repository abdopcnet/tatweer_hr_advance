# File Structure

```
hr_advance/
├── hooks.py
├── api.py
├── event.py
├── tasks.py
├── hr_advance/
│   ├── doctype/
│   │   ├── bank_branch/
│   │   ├── bulk_leave_allocation/
│   │   ├── designation_type/
│   │   ├── employee_bank/
│   │   ├── employee_training_request/
│   │   └── exit_permission_request/
│   ├── report/
│   ├── override/py/
│   │   ├── employee.py
│   │   ├── payroll_entry.py
│   │   └── salary_slip.py
│   └── public/js/
└── custom/
```

## Key Files

- `hooks.py` - App hooks (doctype_js, doc_events, scheduler_events, override_doctype_class)
- `api.py` - Whitelisted API methods
- `event.py` - Document event handlers
- `tasks.py` - Scheduled tasks
- `override/py/` - Core DocType overrides
