#!/usr/bin/env python
import subprocess
import sys

errors = []

# Syntax check
result = subprocess.run(
    ['python', '-m', 'py_compile', 'model.py'],
    capture_output=True, text=True,
    cwd='d:/MahaSena/GeoAlert AI/GeoAlert AI'
)
if result.returncode == 0:
    print('1. Syntax check: PASS')
else:
    print(f'1. Syntax check: FAIL - {result.stderr.strip()[:100]}')
    errors.append('syntax')

# Focused test
result = subprocess.run(
    ['python', '-m', 'pytest',
     'tests/test_attachments.py::TestTicketCompatibility::test_ticket_data_contains_safe_fields',
     '-x', '-v'],
    capture_output=True, text=True,
    cwd='d:/MahaSena/GeoAlert AI/GeoAlert AI'
)
if 'PASSED' in result.stdout:
    print('2. Focused attachment test: PASS')
else:
    print(f'2. Focused attachment test: FAIL - {result.stdout[:200]}')
    errors.append('focused_test')

# Full test suite
result = subprocess.run(
    ['python', '-m', 'pytest', '-x', '-q'],
    capture_output=True, text=True,
    cwd='d:/MahaSena/GeoAlert AI/GeoAlert AI'
)
# Count passed tests from output
import re
matches = re.findall(r'(\d+) passed', result.stdout)
if matches:
    count = int(matches[0])
    print(f'3. Full test suite: PASS - {count} tests passed')
else:
    print(f'3. Full test suite: {"PASS" if result.returncode == 0 else "FAIL"}')
    errors.append('full_suite')

# Summarize
print()
if errors:
    print(f'Errors encountered: {errors}')
    sys.exit(1)
else:
    print('All checks passed!')
    sys.exit(0)