with open('model.py', 'r') as f:
    content = f.read()

checks = {
    'LiDAR Intensity Histogram': 'LiDAR Intensity Histogram' in content,
    'Histogram (go.Histogram)': 'go.Histogram' in content,
    'Synthetic disclaimer': 'synthetic LiDAR intensity distribution' in content,
    'Risk Level Gauge': 'Risk Level (%)' in content,
    'Factor of Safety Gauge': 'Average Factor of Safety' in content,
    'go.Indicator (gauge)': 'go.Indicator' in content,
}

for check, result in checks.items():
    status = 'PASS' if result else 'FAIL'
    print(f'  [{status}] {check}')

print()
print('Positions:')
pos_risk_prop = content.find('st.markdown("### Risk Proportion")')
pos_lidar = content.find('LiDAR Intensity Histogram')
pos_risk_gauge = content.find('Risk Level (%)')
pos_fs_gauge = content.find('Average Factor of Safety')

print(f'  Risk Proportion: {pos_risk_prop}')
print(f'  LiDAR Histogram: {pos_lidar}')
print(f'  Risk Level Gauge: {pos_risk_gauge}')
print(f'  Factor of Safety Gauge: {pos_fs_gauge}')

if pos_risk_prop >= 0 and pos_lidar >= 0 and pos_risk_gauge >= 0 and pos_fs_gauge >= 0:
    order_ok = pos_risk_prop < pos_lidar < pos_risk_gauge < pos_fs_gauge
    print(f'  Order correct: {order_ok}')