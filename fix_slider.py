with open('model.py', 'r') as f:
    c = f.read()

# Remove the broken fs_threshold slider at lines around 1067-1068
# Pattern: "            fs_threshold = st.slider(\n                {mine_type} - Prediction Results Summary")"
# We need to find this and remove it, along with the opening line

# Find the st.slider line
idx = c.find('fs_threshold = st.slider')
print("Found fs_threshold at index:", idx)

if idx >= 0:
    # Find the end of this st.slider call - look for the matching closing paren
    after_slider = c[idx:]
    paren_count = 0
    end_idx = -1
    for i, ch in enumerate(after_slider):
        if ch == '(':
            paren_count += 1
        elif ch == ')':
            paren_count -= 1
            if paren_count == 0:
                end_idx = idx + i + 1
                break
    
    if end_idx > 0:
        # Also check if there's a newline and {mine_type} pattern after the slider
        after_slider_end = c[end_idx:]
        # Look for the {mine_type} pattern that's the broken label
        label_idx = after_slider_end.find('{mine_type}')
        if label_idx >= 0:
            # Remove from idx to end_idx + the label line
            # Find the end of the {mine_type} line
            label_line_end = after_slider_end.find('\n', label_idx)
            if label_line_end >= 0:
                total_end = end_idx + label_line_end + 1
                print("Removing broken slider block from", idx, "to", total_end)
                new_c = c[:idx] + c[total_end:]
                with open('model.py', 'w') as f:
                    f.write(new_c)
                print('Fixed! Removed broken slider block')
            else:
                # No newline found, just remove up to some reasonable point
                new_c = c[:idx] + c[end_idx+label_idx+15:]
                with open('model.py', 'w') as f:
                    f.write(new_c)
                print('Fixed partially')
        else:
            print("{mine_type} label not found after slider")
    else:
        print("Could not find slider end")
else:
    print("fs_threshold slider not found")