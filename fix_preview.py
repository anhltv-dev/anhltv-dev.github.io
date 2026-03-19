import re

with open('index.html', 'r', encoding='utf-8') as f:
    hc = f.read()

count = 0

def fix_drive_preview(match):
    global count
    original_iframe = match.group(0)
    data_src = match.group(1)
    
    if 'drive.google.com' not in data_src:
        return original_iframe
        
    file_id = None
    m = re.search(r'open\?id=([a-zA-Z0-9_-]+)', data_src)
    if m:
        file_id = m.group(1)
        
    if not file_id:
        m = re.search(r'file/d/([a-zA-Z0-9_-]+)', data_src)
        if m:
            file_id = m.group(1)
            
    if file_id:
        new_url = f"https://drive.google.com/file/d/{file_id}/preview"
        if new_url != data_src:
            count += 1
            return original_iframe.replace(data_src, new_url)
    
    return original_iframe

hc = re.sub(r'<iframe[^>]*data-src="([^"]+)"', fix_drive_preview, hc)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(hc)

print(f"Fixed {count} Drive iframe URLs.")
