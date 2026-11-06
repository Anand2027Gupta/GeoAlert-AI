with open('model.py', 'r', newline='') as f:
    content = f.read()

# The old Alerts section to replace - find it
# It starts with 'elif section == "Alerts":' and ends before 'elif section == "Upload Data"'

old_marker = 'elif section == "Alerts":'
new_marker = 'elif section == "Upload Data":'

old_start = content.find(old_marker)
new_start = content.find(new_marker)

if old_start >= 0 and new_start >= 0:
    old_section = content[old_start:new_start]
    print(f"Found old section from {old_start} to {new_start}, length: {len(old_section)}")
    print("OLD section preview (first 200 chars):", old_section[:200])
else:
    print(" markers not found")
    if old_start >= 0:
        print(f"old_marker at {old_start}")
    if new_start >= 0:
        print(f"new_marker at {new_start}")