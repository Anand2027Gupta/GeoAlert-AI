with open('model.py', 'r') as f:
    c = f.read()

import re

# Search for metrics-related content
patterns = [
    r'st\.\w+.*?[Mm]etric',
    r'Total\s+Alert',
    r'Critical\s+count',
    r'High\s+Severity',
    r'severity_distribution',
    r'Top\s+Critical',
    r'alert.*?log|log.*?alert',
]

for pat in patterns:
    matches = re.findall(pat, c, re.IGNORECASE | re.DOTALL)
    if matches:
        print(f'Pattern "{pat}": Found {len(matches)} match(es)')
        for m in matches[:3]:
            # Print first 200 chars of each match
            print(f'  -> {m[:200]}')
    else:
        print(f'Pattern "{pat}": No matches')