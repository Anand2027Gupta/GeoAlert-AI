#!/usr/bin/env python
with open('model.py', 'r') as f:
    content = f.read()

# Check for key elements
checks = {
    'LiDAR Intensity Histogram': 'LiDAR Intensity Histogram' in content,
    'Risk Level Gauge': 'Risk Level (%)' in content,
    'Factor of Safety Gauge': 'Factor of Safety' in content,
    'Safe color (#28a745)': '#28a745' in content,
    'Warning color (#ffc107)': '#ffc107' in content,
    'Critical color (#dc3545)': '#dc3545' in content,
    'Synthetic data disclaimer': 'synthetic LiDAR intensity distribution' in content,
    'metric_card function': 'def metric_card' in content,
}

print('=== Key element verification ===')
for name, result in checks.items():
    status = 'PASS' if result else 'FAIL'
    print(f'{status}: {name}')

print()

# Check that the original News section is removed
original_news = 'Real-Time Indian Mining News' in content
news_status = 'REMOVED' if not original_news else 'STILL PRESENT'
print(f'News section: {news_status}')

# Check AI Assistant section is still present
ai_assistant = 'AI Assistant' in content
ai_status = 'PRESENT' if ai_assistant else 'MISSING'
print(f'AI Assistant section: {ai_status}')