#!/usr/bin/env python3
import re

with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the dummy style block
dummy = 'st.markdown("""<style>\n</style>""", unsafe_allow_html=True)'
if dummy in content:
    content = content.replace(dummy, '')
    print('Removed dummy style block')

# Remove the first inline style block (sidebar radio with #4285F4)
# Find and remove the block from "/* Sidebar radio container */" to the next blank line pattern
block1_pattern = r'/\* Sidebar radio container \*/\s*section\[data-testid="stSidebar"\] div\[role="radiogroup"\] \{\s*/\*gap: 10px;\*/\s*\n\s*Each radio option label \*/\s*section\[data-testid="stSidebar"\] div\[role="radiogroup"\] label \{\s*background-color: #4285F4;\s*box-shadow: 10px 10px 10px grey;\s*padding: 10px 10px;\s*:\\\WINDOWS\\\System32\\\WindowsPowerShell\\\v1.0\\\powershell.exe\u001b\\(.venv'

# Remove the sticky title style block
block2 = '''st.markdown("""<style>\n\n/* Sticky title styles */\n.sticky-title h1 {\n  color: var(--sb-on-surface) !important;\n  font-family: "Inter", sans-serif !important;\n  font-weight: 600 !important;\n  letter-spacing: -0.01em !important;\n}\n\n/* Adjusting the rest of the content so it doesn't get hidden under the title */\n.content-spacer {\n  margin-top: 0px;\n}\n\n/* The sticky container for the title */\n.sticky-title {\n  position: fixed;\n  top: 0;\n  left: 0;\n  width: 100%;\n  height:15%;\n  padding: 30px 30px;\n  z-index: 999;\n  text-align: center;\n  margin: 0;\n  font-size: 30px; /* Slightly reduced as requested */\n  color: #06038D;\n  font-weight: bold;\n  text-align: center;\n  position: fixed;\n  background-color: #f0f2f6;\n}\n\n/* Adjusting the rest of the content so it doesn't get hidden under the title */\n.main .block-container {\n  padding-top: 2em;\n}\n\"\"\", unsafe_allow_html=True)'''

# Remove the second sidebar radio block (with #f0f8ff etc)
block3 = '''st.markdown("""<style>\nsection[data-testid="stSidebar"] label[data-baseweb="radio"] {\n    background-color: #f0f8ff; color: #003366;\n    padding: 10px 16px; border-radius: 8px;\n    border: 1px solid #cce0ff; margin-bottom: 6px;\n    font-size: 18px; font-weight: 600;\n}\nsection[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {\n    background-color: #cce6ff; border-color: #3399ff;\n}\nsection[data-testid="stSidebar"] label[data-baseweb="radio"][aria-checked="true"] {\n    background-color: #007bff; color: white !important; border-color: #0056b3;\n}\n</style>\"\"\", unsafe_allow_html=True)'''

# Remove block 1 (sidebar radio with #4285F4)
# Find the pattern and remove it
start_marker = '/* Sidebar radio container */'
end_marker = '/* Hover effect */'

idx1 = content.find(start_marker)
if idx1 >= 0:
    idx2 = content.find(end_marker, idx1)
    if idx2 >= 0:
        # Find the complete block including the style tags
        block_start = content.rfind('"""', 0, idx1)
        if block_start >= 0:
            block_end = content.find('"""', idx2) + 3
            if block_end > block_start:
                content = content[:block_start] + content[block_end:]
                print(f'Removed block 1: sidebar radio (#4285F4)')

# Remove block 2 (sticky title styles)
start_marker2 = '/* Sticky title styles */'
idx1 = content.find(start_marker2)
if idx1 >= 0:
    # Find the opening and closing triple quotes
    lines = content.split('\n')
    # Find start line
    start_line = 0
    for i, line in enumerate(lines):
        if start_marker2 in line:
            start_line = i
            break
    # Find the triple quote start
    quote_count = 0
    start_quote_idx = -1
    for i in range(start_line, min(start_line + 20, len(lines))):
        if '"""' in lines[i]:
            if start_quote_idx == -1:
                start_quote_idx = i
            else:
                # Found closing
                end_quote_idx = i
                content = '\n'.join(lines[:start_quote_idx]) + '\n'.join(lines[end_quote_idx+1:])
                print(f'Removed block 2: sticky title styles')
                break

# Write back
with open('model.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')