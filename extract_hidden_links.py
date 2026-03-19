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
    
    # Extract from hyperlink target. Sometimes it's in the cell, sometimes it's plain text.
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
            'yt': yt_link
        })

print(f"Extracted {len(topics)} topics with valid URLs")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the actual replacements like before
cards = html.split('<div class=\"topic-card\"')

def get_embed_html(drive, yt):
    res = '<div class="embed-row">\n'
    if drive:
        preview_url = drive.replace('/view?usp=sharing', '/preview').replace('/edit?usp=sharing', '/preview')
        if 'open?id=' in preview_url:
            preview_url = preview_url.replace('open?id=', 'file/d/') + '/preview'
        res += f'''          <div class="embed-panel">
            <div class="embed-label">Tài liệu hướng dẫn</div>
            <div class="embed-frame">
              <iframe data-src="{preview_url}" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" allowfullscreen></iframe>
            </div>
          </div>\n'''
    if yt:
        yt_embed = yt
        if 'watch?v=' in yt:
            yt_embed = yt.replace('watch?v=', 'embed/')
        elif 'youtu.be/' in yt:
            yt_embed = yt.replace('youtu.be/', 'www.youtube.com/embed/')
        res += f'''          <div class="embed-panel">
            <div class="embed-label">Video Bài Giảng</div>
            <div class="embed-frame">
              <iframe data-src="{yt_embed}" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" allowfullscreen></iframe>
            </div>
          </div>\n'''
    res += '        </div>'
    return res

def get_buttons_html(drive, yt):
    res = '<div class="resources">\n'
    if drive:
        res += f'          <a class="chip-link drive" href="{drive}" target="_blank">📁 Tài liệu hệ thống</a>\n'
    if yt:
        res += f'          <a class="chip-link youtube" href="{yt}" target="_blank">▶ Video giới thiệu</a>\n'
    res += '        </div>'
    return res

new_html = cards[0]
updated_count = 0

for i in range(1, len(cards)):
    card = '<div class="topic-card"' + cards[i]
    title_match = re.search(r'<div class="topic-title">(.*?)</div>', card)
    if not title_match:
        new_html += card
        continue
        
    html_title = title_match.group(1).lower().strip()
    
    matched = None
    for t in topics:
        if html_title in t['title'] or t['title'] in html_title:
            matched = t
            break
            
    if matched:
        pattern = r'<div class="embed-row">.*?<div class="resources">.*?</a>\s*</div>'
        replacement = get_embed_html(matched['drive'], matched['yt']) + '\n        ' + get_buttons_html(matched['drive'], matched['yt'])
        new_card = re.sub(pattern, replacement, card, flags=re.DOTALL)
        if new_card != card:
            updated_count += 1
            card = new_card
            
    new_html += card

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
    
print(f"Updated HTML file, {updated_count} cards changed.")
