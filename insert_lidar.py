import re

with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find "Risk Proportion" section to add LiDAR histogram after it
idx = content.find('st.markdown("### Risk Proportion")')
if idx >= 0:
    after = content[idx:idx+2000]
    next_section = re.search(r'st\.(subheader|markdown\("###")', after)
    if next_section:
        insert_pos = idx + next_section.start()
    else:
        insert_pos = idx + 2000
    
    # LiDAR Intensity Histogram section to insert
    lidar_section = '''\n\n    # LiDAR Intensity Histogram\n    st.subheader("LiDAR Intensity Histogram")\n    \n    # Synthetic demonstration data\n    np.random.seed(42)\n    lidar_intensity = np.random.normal(loc=128, scale=40, size=100)\n    lidar_intensity = np.clip(lidar_intensity, 0, 255).astype(int)\n    \n    fig = go.Figure(data=[go.Histogram(x=lidar_intensity, nbins=20, marker_color="#1f77b4")])\n    fig.update_layout(\n        paper_bgcolor="#0d1322",\n        plot_bgcolor="#0d1322",\n        font_color="#dde2f8",\n        showlegend=False,\n        title_text="LiDAR Intensity Distribution",\n        xaxis_title="Intensity Value",\n        yaxis_title="Frequency",\n        height=400,\n    )\n    \n    # Add disclaimer for synthetic data\n    st.caption("Demo only \u2014 synthetic LiDAR intensity distribution; not real sensor measurements.")\n    \n    st.plotly_chart(fig, use_container_width=True)\n\n'''
    
    new_content = content[:insert_pos] + lidar_section + content[insert_pos:]
    
    with open('model.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"LiDAR section inserted at position {insert_pos}")
else:
    print("Could not find 'Risk Proportion' section")