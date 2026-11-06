import os
sz = os.path.getsize("model.py")
print("File size:", sz)

with open("model.py", "r") as f:
    c = f.read()

# Find FS Threshold
idx = c.find("FS Threshold")
print("FS Threshold at index:", idx if idx >= 0 else "Not found")

# Find elif section == "Results"
marker = 'elif section == "Results"'
idx2 = c.find(marker)
print('Results marker at index:', idx2 if idx2 >= 0 else "Not found")

# Print surrounding context
if idx >= 0 and idx2 > idx:
    print("\nContext around FS Threshold:")
    print(c[idx:idx+200])
    print("\nContext around Results marker:")
    print(c[idx2:idx2+200])