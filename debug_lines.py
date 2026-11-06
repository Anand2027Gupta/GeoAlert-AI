with open('model.py', 'r', newline='') as f:
    lines = f.readlines()

# Print lines 930-950 for verification
for i in range(929, min(951, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")