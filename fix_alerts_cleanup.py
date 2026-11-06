import re

with open('model.py', 'r') as f:
    c = f.read()

# Find and remove the old Alerts section code (from FS Threshold through end of section)
old_marker = 'FS Threshold (Lower Bound)'
old_start = c.find(old_marker)

# Find the Results section marker
results_marker = 'elif section == "Results"'
results_start = c.find(results_marker)

if old_start >= 0 and results_start > old_start:
    # Remove the old section
    new_c = c[:old_start] + c[results_start:]
    with open('model.py', 'w') as f:
        f.write(new_c)
    print('Old Alerts section removed successfully')
else:
    print('Could not find markers for removal')
    print(f"old_start: {old_start}, results_start: {results_start}")