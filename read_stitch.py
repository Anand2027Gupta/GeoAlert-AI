with open('d:/MahaSena/GeoAlert AI/GeoAlert AI/stitch_geoalert_ai_mining_dashboard/stitch_geoalert_ai_mining_dashboard/mining_intelligence_overview/code.html', 'r') as f:
    content = f.read()
idx = content.find('pt-20"')
if idx > 0:
    print(content[idx:idx+3000])