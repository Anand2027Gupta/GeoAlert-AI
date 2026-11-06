# Restore model.py to a working state with Stage C Overview fixes

with open('model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Clean up: remove lines that cause syntax errors (the problematic inserted sections)
# Keep only the core: metric_card function, KPI grid, risk trend chart, and original monitoring sections

# Find and remove from the first problematic st.divider() after the risk chart section
# to the end of the file, then selectively keep only the core sections

# Strategy: rebuild the file from scratch with only the verified working sections

# The core structure we want:
# 1. Imports (lines 1-20)
# 2. metric_card function (lines 447-456, updated)
# 2. Overview section (lines 472-520ish, with KPI grid + risk chart)
# 3. Original Open-Pit/Underground monitoring sections (preserved)

# Let me just verify the key sections are correct and test

# Check metric_card function
idx = content.find('def metric_card')
if idx >= 0:
    print("metric_card function found")
else:
    print("metric_card function NOT found")

# Check KPI grid
if 'metric_card("Current Risk"' in content:
    print("KPI grid with metric_card found")
else:
    print("KPI grid with metric_card NOT found")

# Check risk trend chart
if 'Risk Trend Analysis' in content:
    print("Risk trend chart found")
else:
    print("Risk trend chart NOT found")

# Check original monitoring sections
if 'Open Pit Stability Trends' in content:
    print("Open-Pit monitoring preserved")
else:
    print("Open-Pit monitoring NOT preserved")

if 'Underground Seismic' in content or 'Underground Monitoring' in content:
    print("Underground monitoring preserved")
else:
    print("Underground monitoring NOT preserved")

print(f"\nFile size: {len(content)} characters")
print(f"Total lines: {len(lines)}")
"