import re

with open('model.py', 'r') as f:
    c = f.read()

# Remove the broken fs_threshold slider code
# Pattern: fs_threshold = st.slider(\n                {mine_type} - Prediction Results Summary")
old_pattern = 'fs_threshold = st.slider(\n                {mine_type} - Prediction Results Summary")'
print("Looking for pattern:", repr(old_pattern[:50]))

# Try to find and remove
idx = c.find('fs_threshold = st.slider')
print("Found fs_threshold at:", idx)

if idx >= 0:
    # Find the closing parenthesis of st.slider
    # Look for the pattern after the slider start
    slider_start = idx
    # Find where the slider argument ends - look for ")" that closes st.slider(
    remaining = c[slider_start:]
    # Find the closing paren
    paren_count = 0
    found_end = -1
    for i, ch in enumerate(remaining):
        if ch == '(':
            paren_count += 1
        elif ch == ')':
            paren_count -= 1
            if paren_count == 0:
                found_end = slider_start + i + 1
                break
    
    if found_end > 0:
        print("Found slider end at:", found_end)
        # Remove from slider_start to found_end
        new_c = c[:slider_start] + c[found_end:]
        # Also clean up extra blank lines
        new_c = re.sub(r'\n\n\n+', '\n\n', new_c)
        with open('model.py', 'w') as f:
            f.write(new_c)
        print('Fixed! Removed', found_end - slider_start, 'characters')
    else:
        print("Could not find slider end")
else:
    print("fs_threshold slider not found")