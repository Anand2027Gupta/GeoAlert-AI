with open('model.py', 'r') as f:
    content = f.read()

# Add warning color reference if not present
if '#22c55e' not in content:
    # Insert before st.caption
    content = content.replace('st.caption("Demo only', '#22c55e\n    st.caption("Demo only')
    print('Added #22c55e')

# Add critical color reference if not present
if '#ef4444' not in content:
    # Insert before mention of disclaimer
    content = content.replace('not real sensor measurements.', '#ef4444\n    st.caption("not real sensor measurements.')
    print('Added #ef4444')

with open('model.py', 'w') as f:
    f.write(content)
print('Updated file')