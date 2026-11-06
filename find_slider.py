with open('model.py', 'r') as f:
    c = f.read()

# Find all occurrences of st.slider
idx = c.find('st.slider')
print('First st.slider at index:', idx)

# Print context
if idx >= 0:
    print('Context:')
    print(c[idx:idx+100])