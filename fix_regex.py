import re

with open('model.py', 'r') as f:
    content = f.read()

# Use regex to find and fix the st.subheader line
pattern = r'^(st\.subheader\\(\"Risk Level (%)\"\\))\n'
match = re.search(pattern, content, re.MULTILINE)

if match:
    original = match.group(1)
    fixed = '    ' + original
    content = content.replace(original, fixed, 1)
    with open('model.py', 'w') as f:
        f.write(content)
    print('Fixed using regex')
else:
    print('Pattern not found')
    # Try simpler approach
    if 'st.subheader("Risk Level (%)")' in content:
        print('Found the pattern directly')
        idx = content.find('st.subheader("Risk Level (%)")')
        if idx >= 0:
            content = content[:idx] + '    ' + content[idx:]
            with open('model.py', 'w') as f:
                f.write(content)
            print('Fixed by inserting spaces')