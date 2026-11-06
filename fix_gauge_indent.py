import re

with open('model.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the Risk Level gauge section indentation
# The issue is that st.subheader("Risk Level (%)") has 0 spaces but should have 4

# Find and replace the problematic section
old_code = """st.subheader("Risk Level (%)")

    # Calculate risk percentage from data
    risk_percent = min(data['rockfall_risk'].mean() * 100, 100) if 'rockfall_risk' in data.columns else 0

    fig_risk = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Level (%)"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#ffb690"},
            'steps': [
                {'range': [0, 33], 'color': "#28a745"},
                {'range': [33, 66], 'color': "#ffc107"},
                {'range': [66, 100], 'color': "#dc3545"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))

    fig_risk.update_layout(
        paper_bgcolor="#0d1322",
        plot_bgcolor="#0d1322",
        font_color="#dde2f8",
        height=300,
    )

    st.plotly_chart(fig_risk, use_container_width=True)"""

new_code = """    st.subheader("Risk Level (%)")

    # Calculate risk percentage from data
    risk_percent = min(data['rockfall_risk'].mean() * 100, 100) if 'rockfall_risk' in data.columns else 0

    fig_risk = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_percent,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Level (%)"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#ffb690"},
            'steps': [
                {'range': [0, 33], 'color': "#28a745"},
                {'range': [33, 66], 'color': "#ffc107"},
                {'range': [66, 100], 'color': "#dc3545"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))

    fig_risk.update_layout(
        paper_bgcolor="#0d1322",
        plot_bgcolor="#0d1322",
        font_color="#dde2f8",
        height=300,
    )

    st.plotly_chart(fig_risk, use_container_width=True)"""

if old_code in content:
    new_content = content.replace(old_code, new_code)
    with open('model.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed Risk Level gauge section indentation")
else:
    print("Could not find the exact old_code to replace")
    # Debug: find the section
    idx = content.find('st.subheader("Risk Level (%)")')
    print(f"Found at position: {idx}")
    # Show surrounding context
    if idx >= 0:
        print(content[idx-50:idx+100])