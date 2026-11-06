with open('model.py', 'r') as f:
    c = f.read()

# Remove the broken if block (lines with if statement and empty body)
# Find the if statement
idx = c.find('if mine_type == "Open Pit Mines" and is_open_pit_data:')

if idx >= 0:
    # Find the end - look for total_records = len(data) which should stay
    target = '    total_records = len(data)'
    target_idx = c.find(target, idx)
    print('Target at:', target_idx)
    
    if target_idx > idx:
        # Remove from idx to target_idx (exclusive), which removes the if block
        # But we need to also handle the indentation of total_records
        # Currently total_records has 4 spaces indent, which is correct for the function body
        new_c = c[:idx] + c[target_idx:]
        with open('model.py', 'w') as f:
            f.write(new_c)
        print('Removed if block successfully')
    else:
        print('Target not found')
else:
    print('if statement not found')