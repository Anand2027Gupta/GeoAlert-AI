import os
sz = os.path.getsize('model.py')
print('File size:', sz)

with open('model.py', 'r') as f:
    c = f.read()

# Check for FS Threshold old code
idx = c.find('FS Threshold (Lower Bound)')
print('FS Threshold (Lower Bound) at index:', idx if idx >= 0 else 'Not found - GOOD!')

# Check for Results section
idx2 = c.find('elif section == "Results"')
print('Results marker at index:', idx2 if idx2 >= 0 else 'Not found - GOOD!')

# Check for new metrics code
for marker in ['Total Alerts', 'Critical count', 'High Severity count', 'severity_distribution', 'Top Critical Alerts', 'alert log']:
    if marker in c:
        print(f'Found "{marker}" in file')
    else:
        print(f'NOT found "{marker}" in file')