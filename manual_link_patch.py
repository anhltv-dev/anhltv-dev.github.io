import openpyxl
import re

wb = openpyxl.load_workbook('20260305 NDHD BAZIS - WS NESTING THINH PHUC HUNG.xlsx')
ws = wb.active

# Get specific 5 topics
patch_data = {
    "tổng thể hệ thống phần mềm bazis – woodsoft": None,
    "mặt cắt / lát cắt": None,
    "nhập / xuất với phần mềm bên thứ 3": None,
    "sơ đồ lắp đặt": None,
    "làm việc với dự án": None
}

for row in ws.iter_rows(min_row=2):
    if len(row) < 8: continue
        
    title_val = str(row[2].value).strip().lower() if row[2].value else ''
    yt_val = str(row[7].value).strip() if row[7].value else ''
    
    drive_link, yt_link = '', ''
    if row[6].hyperlink: drive_link = row[6].hyperlink.target
    elif row[6].value and 'http' in str(row[6].value): drive_link = str(row[6].value).strip()
    if row[7].hyperlink: yt_link = row[7].hyperlink.target
    elif row[7].value and 'http' in str(row[7].value): yt_link = str(row[7].value).strip()

    if title_val == "tổng thể hệ thống phần mềm bazis- woodsoft":
        patch_data["tổng thể hệ thống phần mềm bazis – woodsoft"] = (drive_link, yt_link)
    elif title_val == "mặt cắt lát cắt":
        patch_data["mặt cắt / lát cắt"] = (drive_link, yt_link)
    elif title_val == "nhập/ xuất với phần mềm bên thứ 3":
        patch_data["nhập / xuất với phần mềm bên thứ 3"] = (drive_link, yt_link)
    elif title_val == "làm việc vơi dự án":
        patch_data["làm việc với dự án"] = (drive_link, yt_link)
    elif yt_val == "SƠ ĐỒ LẮP ĐẶT":
        patch_data["sơ đồ lắp đặt"] = (drive_link, yt_link)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

cards = html.split('<div class="topic-card"')
new_html = cards[0]
updated = 0

for i in range(1, len(cards)):
    card = '<div class="topic-card"' + cards[i]
    m = re.search(r'<div class="topic-title">(.*?)</div>', card)
    if m:
        t = m.group(1).lower().strip()
        if t in patch_data and patch_data[t]:
            drive, yt = patch_data[t]
            pattern = r'<div class="embed-row">.*?<div class="resources">.*?</a>\s*</div>'
            replacement = get_embed_html(drive, yt) + '\n        ' + get_buttons_html(drive, yt)
            card = re.sub(pattern, replacement, card, flags=re.DOTALL)
            updated += 1
            print(f"Patched strictly unmatched topic: {t}")
    new_html += card

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Patched {updated} topics.")
