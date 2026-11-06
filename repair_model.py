#!/usr/bin/env python
"""Repair script for model.py indentation and duplication errors."""

with open('model.py', 'r') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# ==========================================
# Edit 1: Fix metric_card indentation
# ==========================================
# Line 553 (1-based) = lines[552] (0-based): <div style= line
# Line 552 (1-based) = lines[551] (0-based): st.markdown line
# Original had 5 spaces, current has 4 spaces

# Fix line 553 (0-based index 552)
old_line_553 = lines[552]
print(f"Before fix - line 553: {repr(old_line_553)}")
if old_line_553.startswith('    <div style='):
    # Change from 4 spaces to 5 spaces
    lines[552] = '     <div style=' + old_line_553[len('    <div style='):]
    print(f"  Fixed line 553: {repr(lines[552])}")

# Fix line 552 (0-based index 551)
old_line_552 = lines[551]
print(f"Before fix - line 552: {repr(old_line_552)}")
if old_line_552.startswith('    st.markdown'):
    lines[551] = '     st.markdown' + old_line_552[len('    st.markdown'):]
    print(f"  Fixed line 552: {repr(lines[551])}")

# ==========================================
# Edit 2: Remove duplicate LiDAR and old News section
# ==========================================
# Based on analysis:
# - Line 1454 (1-based): st.plotly_chart(fig_fs, use_container_width=True) - KEEP (0-based: 1453)
# - Lines 1456-1480 (1-based): duplicate LiDAR Histogram - REMOVE (0-based: 1455-1479)
# - Lines 1482-1501 (1-based): old News section with adjusted_risk_percent - REMOVE (0-based: 1481-1501)
# - After removal, line 1454 (0-based 1453) should connect to elif section

# Remove lines 1456-1501 (1-based) = indices 1455-1500 (0-based)
# This removes: duplicate LiDAR + empty line + old news section

# Let me first check what's at these positions
print("\nChecking lines around removal area (1-based):")
for i in range(1453, 1510):
    if i < len(lines):
        print(f"  {i+1}: {lines[i].rstrip()[:60]}")

# Remove indices 1455 through 1500 inclusive (0-based)
# That's 46 lines to remove
if len(lines) > 1500:
    # Remove lines 1455 to 1500 (0-based) = 1456 to 1501 (1-based)
    del lines[1455:1501]
    print(f"\nRemoved 46 lines (indices 1455-1500 inclusive)")
    print(f"New total lines: {len(lines)}")

# ==========================================
# Edit 3: Verify the flow after fix
# ==========================================
print("\nChecking lines around the fix area (1-based):")
for i in range(1450, 1470):
    if i < len(lines):
        print(f"  {i+1}: {lines[i].rstrip()[:60]}")

# Write the fixed file
with open('model.py', 'w') as f:
    f.writelines(lines)

print("\nFile repaired successfully!")