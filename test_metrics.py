with open('model.py', 'r') as f:
    c = f.read()

checks = [
    'Total Alerts',
    'Critical count', 
    'High Severity count',
    'severity_distribution',
    'Top Critical Alerts',
    'alert log',
    'FS Threshold (Lower Bound)',
]

for check in checks:
    found = check in c
    print(f'{check}: {"FOUND" if found else "NOT FOUND"}')