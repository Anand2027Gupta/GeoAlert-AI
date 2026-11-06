with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find metric_card function
idx = content.find('def metric_card')
if idx > 0:
    print('=== metric_card function ===')
    print(content[idx:idx+200])
    print()

# Find the Overview section
idx = content.find('if section == "Overview"')
if idx > 0:
    print('=== Overview section start ===')
    print(content[idx:idx+500])
    print()

# Find the KPI grid
idx = content.find('2x2')
if idx > 0:
    print('=== KPI grid area ===')
    start = max(0, idx-100)
    end = min(len(content), idx+200)
    print(content[start:end])