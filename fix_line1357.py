with open('model.py', 'r') as f:
    lines = f.readlines()

# Fix line 1357 - change 8 spaces to 4 spaces before st.subheader
if len(lines) > 1356:
    old = lines[1356]
    new = '    st.subheader("LiDAR Intensity Histogram")\n'
    if old != new:
        lines[1356] = new
        with open('model.py', 'w') as f:
            f.writelines(lines)
        print('Fixed line 1357 indentation')
    else:
        print('Already correct')