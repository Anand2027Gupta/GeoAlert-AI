with open('model.py', 'r') as f:
    content = f.read()

old = 'st.subheader("LiDAR Intensity Histogram")'
new = '    st.subheader("LiDAR Intensity Histogram")'

if old in content:
    content = content.replace(old, new, 1)
    with open('model.py', 'w') as f:
        f.write(content)
    print('Fixed LiDAR subheader indentation')
else:
    print('Pattern not found')