#!/usr/bin/env python
with open('model.py', 'r') as f:
    content = f.read()

# Fix line 1380 - the string needs proper closing
# Replace the broken line
old = '    st.caption("Demo only – synthetic LiDAR intensity distribution; #ef4444\n'
new = '    st.caption("Demo only – synthetic LiDAR intensity distribution; #ef4444")\n'

if old in content:
    content = content.replace(old, new)
    print(f"Replaced broken string line")
else:
    print("Old string not found, trying alternative...")
    # Try without the em dash issue
    old2 = '    st.caption("Demo only '
    # Find and fix the string
    idx = content.find('st.caption("Demo only')
    if idx >= 0:
        # Find the end of this string
        end_quote = content.find('"', idx + 1)
        print(f"Found st.caption at {idx}, next quote at {end_quote}")
        print(f"Context: {repr(content[idx:end_quote+20])}")

with open('model.py', 'w') as f:
    f.write(content)
print("Done")