#!/usr/bin/env python
import sys

try:
    with open('model.py', 'r') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    changes = []
    
    # ==========================================
    # Fix 1: metric_card indentation (lines 552-553, 1-based)
    # ==========================================
    # Line 552 (1-based) = lines[551] (0-based): st.markdown should have 4 spaces
    # Line 553 (1-based) = lines[552] (0-based): <div style= should have 5 spaces
    
    # Fix line 552 - st.markdown
    if len(lines) > 551 and lines[551].startswith('     st.markdown'):
        lines[551] = '    st.markdown' + lines[551][5:]
        changes.append("Fix1: st.markdown indent 5->4")
    
    # Fix line 553 - <div style=
    if len(lines) > 552 and lines[552].startswith('     <div style='):
        changes.append("Fix2: <div style= already 5 spaces")
    elif len(lines) > 552:
        # Ensure it's 5 spaces
        if lines[552].startswith('    <div style='):
            lines[552] = '     <div style=' + lines[552][4:]
            changes.append("Fix3: <div style= indent 4->5")
    
    # ==========================================
    # Fix 2: Line 1383 - st.subheader indent (1-based)
    # ==========================================
    # Current: 12 spaces, should be 4 spaces
    
    if len(lines) > 1382 and lines[1382].startswith('            st.subheader'):
        lines[1382] = '    st.subheader("Risk Level (%)")\n'
        changes.append("Fix4: subheader indent 12->4")
    
    # ==========================================
    # Fix 3: Remove duplicate LiDAR and old News section
    # ==========================================
    # Find LiDAR occurrences
    lidar_positions = [i for i, line in enumerate(lines) if 'LiDAR Intensity Histogram' in line]
    
    print(f"LiDAR positions (0-based): {lidar_positions}")
    
    if len(lidar_positions) >= 2:
        second_liadard = lidar_positions[1]
        # Find AI Assistant section
        ai_assistant_line = None
        for i in range(second_liadard, len(lines)):
            if 'elif section == "AI Assistant":' in lines[i]:
                ai_assistant_line = i
                break
        
        print(f"Second LiDAR at: {second_liadard}, AI Assistant at: {ai_assistant_line}")
        
        if ai_assistant_line:
            # Remove from second LiDAR to AI Assistant inclusive
            removed = len(lines[second_liadard:ai_assistant_line+1])
            del lines[second_liadard:ai_assistant_line+1]
            changes.append(f"Fix5: Removed {removed} lines (duplicate LiDAR + News + adjusted_risk)")
    
    # ==========================================
    # Write the fixed file
    # ==========================================
    with open('model.py', 'w') as f:
        f.writelines(lines)
    
    print(f"\nTotal fixes applied: {len(changes)}")
    for c in changes:
        print(f"  - {c}")
    print(f"New total lines: {len(lines)}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()