#!/usr/bin/env python
with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for key visual elements
checks = {
    'metric_card function': 'def metric_card' in content,
    '2x2 KPI grid': '2x2' in content,
    'Overview section': 'if section == "Overview"' in content,
    'Current Risk metric': 'Current Risk' in content,
    'Active Alerts metric': 'Active Alerts' in content,
    'System Status metric': 'System Status' in content,
    'Last Analyzed metric': 'Last Analyzed' in content,
    'Risk trend chart': 'risk trend' in content.lower() or 'Risk Trend' in content,
    'LiDAR heatmap': 'LiDAR Terrain Heatmap' in content,
    'Synthetic demo label': 'synthetic distribution for demonstration' in content,
    'Progress rings/gauges': 'gauge' in content.lower(),
    'CRITICAL badge': 'CRITICAL' in content,
    'HIGH badge': 'HIGH' in content,
    'Help Desk Attachment_Display': 'Attachment_Display' in content,
    'save_helpdesk_attachment': 'save_helpdesk_attachment' in content,
}

for check, result in checks.items():
    status = 'PASS' if result else 'FAIL'
    print(f'  [{status}] {check}')

print()
all_pass = all(checks.values())
print(f'All checks pass: {all_pass}')