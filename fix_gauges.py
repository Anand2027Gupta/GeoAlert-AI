import re

with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the LiDAR Intensity Histogram section and add gauges after it
lidar_marker = 'LiDAR Intensity Histogram'
idx = content.find(lidar_marker)
if idx >= 0:
    # Find the end of the LiDAR section (look for next st.subheader or major section)
    after = content[idx:idx+3000]
    # Find the next st.subheader after the LiDAR section
    next_section = re.search(r'st\.(subheader|markdown\("###")', after)
    if next_section:
        insert_pos = idx + next_section.start()
    else:
        insert_pos = idx + 3000
    
    # Gauges section to insert
    gauges_section = '''\n\n    # Risk Level Gauge\n    st.subheader("Risk Level (%)")\n    \n    # Calculate risk percentage from data\n    risk_percent = min(data['rockfall_risk'].mean() * 100, 100) if 'rockfall_risk' in data.columns else 0\n    \n    fig_risk = go.Figure(go.Indicator(\n        mode = "gauge+number",\n        value = risk_percent,\n        domain = {'x': [0, 1], 'y': [0, 1]},\n        title = {'text': "Risk Level (%)"},\n        gauge = {\n            'axis': {'range': [None, 100]},\n            'bar': {'color': "#ffb690"},\n            'steps': [\n                {'range': [0, 33], 'color': "#28a745"},\n                {'range': [33, 66], 'color': "#ffc107"},\n                {'range': [66, 100], 'color': "#dc3545"}\n            ],\n            'threshold': {\n                'line': {'color': "white", 'width': 4},\n                'thickness': 0.75,\n                'value': 100\n            }\n        }\n    ))\n    \n    fig_risk.update_layout(\n        paper_bgcolor="#0d1322",\n        plot_bgcolor="#0d1322",\n        font_color="#dde2f8",\n        height=300,\n    )\n    \n    st.plotly_chart(fig_risk, use_container_width=True)\n    \n    # Average Factor of Safety Gauge\n    st.subheader("Average Factor of Safety")\n    \n    # Calculate average Factor of Safety from data\n    avg_fs = round(data['fs'].mean(), 2) if 'fs' in data.columns else 0\n    min_fs = round(data['fs'].min(), 2) if 'fs' in data.columns else 0\n    max_fs = round(data['fs'].max(), 2) if 'fs' in data.columns else 0\n    \n    fig_fs = go.Figure(go.Indicator(\n        mode = "gauge+number",\n        value = avg_fs,\n        domain = {'x': [0, 1], 'y': [0, 1]},\n        title = {'text': "Average Factor of Safety"},\n        gauge = {\n            'axis': {'range': [min_fs * 0.8, max_fs * 1.2] if max_fs > min_fs else [0, 3]},\n            'bar': {'color': "#1f77b4"},\n            'steps': [\n                {'range': [0, 1], 'color': "#28a745"},\n                {'range': [1, 2], 'color': "#ffc107"},\n                {'range': [2, 3], 'color': "#dc3545"}\n            ],\n            'threshold': {\n                'line': {'color': "white", 'width': 4},\n                'thickness': 0.75,\n                'value': max_fs\n            }\n        }\n    ))\n    \n    fig_fs.update_layout(\n        paper_bgcolor="#0d1322",\n        plot_bgcolor="#0d1322",\n        font_color="#dde2f8",\n        height=300,\n    )\n    \n    st.plotly_chart(fig_fs, use_container_width=True)\n\n'''
    
    new_content = content[:insert_pos] + gauges_section + content[insert_pos:]
    
    with open('model.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Gauges section inserted at position {insert_pos}")
else:
    print("Could not find 'LiDAR Intensity Histogram' section")