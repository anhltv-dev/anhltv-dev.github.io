import openpyxl
import re
import difflib

wb = openpyxl.load_workbook('20260305 NDHD BAZIS - WS NESTING THINH PHUC HUNG.xlsx')
ws = wb.active

topics = []
for row in ws.iter_rows(min_row=2):
    if len(row) < 8: continue
        
    title = str(row[2].value).strip() if row[2].value else ''
    if not title: continue
    
    drive_link, yt_link = '', ''
    if row[6].hyperlink: drive_link = row[6].hyperlink.target
    elif row[6].value and 'http' in str(row[6].value): drive_link = str(row[6].value).strip()
    if row[7].hyperlink: yt_link = row[7].hyperlink.target
    elif row[7].value and 'http' in str(row[7].value): yt_link = str(row[7].value).strip()
        
    if drive_link or yt_link:
        topics.append({'title': title.lower().strip(), 'drive': drive_link, 'yt': yt_link, 'used': False})

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

cards = html.split('<div class="topic-card"')
html_titles = []
for i in range(1, len(cards)):
    card = '<div class="topic-card"' + cards[i]
    m = re.search(r'<div class="topic-title">(.*?)</div>', card)
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
            print(f'HTML Title strictly unmatched: {t}')
            # Fuzzy match
            titles = [x['title'] for x in topics]
            close = difflib.get_close_matches(t, titles, n=1, cutoff=0.3)
            if close:
                print(f'   -> Fuzzy matched to Excel topic: {close[0]}')
            else:
                print(f'   -> NO MATCH FOUND')

print('---')
for topic in topics:
    if not topic['used']:
        print(f'Excel Topic unused: {topic["title"]}')

