import re
import pandas as pd

excel_file = '20260305 NDHD BAZIS - WS NESTING THINH PHUC HUNG.xlsx'
df = pd.read_excel(excel_file, header=None)

excel_topics = []
for index, row in df.iterrows():
    if index == 0: continue
    title = str(row[1]).strip() if pd.notna(row[1]) else ''
    if not title: continue
    
    drive_link = str(row[5]).strip() if 5 < len(row) and pd.notna(row[5]) else ''
    yt_link = str(row[6]).strip() if 6 < len(row) and pd.notna(row[6]) else ''
    
    if drive_link or yt_link:
        excel_topics.append({
            'title': title.lower().strip(),
            'drive': drive_link,
            'yt': yt_link
        })

print(f"Found {len(excel_topics)} topics with links")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Split HTML by topic card
cards = html.split('<div class="topic-card"')

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

updated_count = 0
new_html = cards[0]

for i in range(1, len(cards)):
    card = cards[i]
    # Reattach split token
    card = '<div class="topic-card"' + card
    
    # Quick regex block replacement inside the card
    # To be safe, only if there's a title inside
    title_match = re.search(r'<div class="topic-title">(.*?)</div>', card)
    if not title_match:
        new_html += card
        continue
        
    html_title = title_match.group(1).lower().strip()
    
    matched = None
    for t in excel_topics:
        if html_title in t['title'] or t['title'] in html_title:
            matched = t
            break
            
    if matched:
        # We need to replace <div class="embed-row">...</div> and <div class="resources">...</div>
        # But wait, python re.sub with DOTALL can be dangerous if there are multiple matches
        # We do it safely
        pattern = r'<div class="embed-row">.*?</div>\s*<div class="resources">.*?</div>'
        replacement = get_embed_html(matched['drive'], matched['yt']) + '\n        ' + get_buttons_html(matched['drive'], matched['yt'])
        
        # We must be extremely careful to only replace the FIRST instance inside this specific topic card
        # Actually our pattern matches across greedy delimiters. Let's use lazy .*?
        # A safer pattern bounds by closing div of resources:
        pattern = r'<div class="embed-row">[\s\S]*?<div class="resources">[\s\S]*?</div>\s*</div>\s*</div>'
        # Wait, the structure is:
        # <div class="embed-row">...</div>
        # <div class="resources">...</div>
        # </div> (closes topic-body)
        # </div> (closes topic-card)
        # So it's easier to just use string splitting or a precise regex
        # precise regex:
        new_card = re.sub(r'<div class="embed-row">.*?<div class="resources">.*?</a>\s*</div>', replacement, card, flags=re.DOTALL)
        if new_card != card:
            updated_count += 1
            card = new_card
            
    new_html += card

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
    
print(f"Updated {updated_count} elements")
