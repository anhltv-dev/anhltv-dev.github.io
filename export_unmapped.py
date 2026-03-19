import openpyxl
import re
import json

wb = openpyxl.load_workbook('20260305 NDHD BAZIS - WS NESTING THINH PHUC HUNG.xlsx')
ws = wb.active

topics = []
for row in ws.iter_rows(min_row=2):
    if len(row) < 8: continue
        
    title_cell = row[2]
    drive_cell = row[6]
    yt_cell = row[7]
    
    title = str(title_cell.value).strip() if title_cell.value else ""
    drive_link = ""
    yt_link = ""
    
    if drive_cell.hyperlink:
        drive_link = drive_cell.hyperlink.target
    elif drive_cell.value and 'http' in str(drive_cell.value):
        drive_link = str(drive_cell.value).strip()
        
    if yt_cell.hyperlink:
        yt_link = yt_cell.hyperlink.target
    elif yt_cell.value and 'http' in str(yt_cell.value):
        yt_link = str(yt_cell.value).strip()
        
    if title and (drive_link or yt_link):
        topics.append({
            'title': title.lower().strip(),
            'drive': drive_link,
            'yt': yt_link,
            'used': False
        })

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

cards = html.split('<div class=\"topic-card\"')
html_titles = []
unmatched_html = []
for i in range(1, len(cards)):
    card = '<div class=\"topic-card\"' + cards[i]
    m = re.search(r'<div class=\"topic-title\">(.*?)</div>', card)
    if m:
        t = m.group(1).lower().strip()
        html_titles.append(t)
        
        matched = False
        for topic in topics:
            if t in topic['title'] or topic['title'] in t:
                topic['used'] = True
                matched = True
                break
        if not matched:
            unmatched_html.append(t)

unused_excel = [t['title'] for t in topics if not t['used']]

with open('unmapped.json', 'w', encoding='utf-8') as f:
    json.dump({'unmatched_html': unmatched_html, 'unused_excel': unused_excel}, f, ensure_ascii=False, indent=2)
