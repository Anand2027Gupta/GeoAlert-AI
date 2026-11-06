#!/usr/bin/env python3
with open('model.py', 'rb') as f:
    c = f.read()

# Update column configuration from 2 to 3 columns
old_col = b'col1, col2 = st.columns(2)'
new_col = b'col1, col2, col3 = st.columns(3)'
c = c.replace(old_col, new_col, 1)

# Update help text for recipient emails
old_help = b'separated by commas.",'
new_help = b'separated by commas. Configure SMTP in Streamlit secrets or environment variables.",'
c = c.replace(old_help, new_help, 1)

with open('model.py', 'wb') as f:
    f.write(c)

print("Model updates complete")