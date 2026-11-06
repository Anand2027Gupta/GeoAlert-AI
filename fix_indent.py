import re

with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix indentation: replace 5 spaces with 4 before '<div style='
content = content.replace('     <div style="', '    <div style="')

with open('model.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed indentation')