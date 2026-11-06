#!/usr/bin/env python
with open('model.py', 'r') as f:
    lines = f.readlines()

# Fix line 1380 (0-based index 1379) - replace corrupted Unicode characters
# The line has: st.caption("Demo only + corrupted + synthetic...
# Replace with proper ASCII

lines[1379] = '    st.caption("Demo only - synthetic LiDAR intensity distribution; #ef4444")\n'

with open('model.py', 'w') as f:
    f.writelines(lines)
print("Fixed line 1380")