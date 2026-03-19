import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject for "Bài tập thực hành 01 & 02"
block_1_pattern = r'(<div class="topic-title">\s*Bài tập thực hành 01 & 02\s*</div>.*?<div class="resources">)'
block_1_inject = r'\n          <a class="chip-link drive" style="background:#f3e8fd; color:#6f42c1; border-color:rgba(107,68,214,0.2)" href="BLV 1.pdf" target="_blank" download>📄 Tải BLV 1.pdf</a>\n          <a class="chip-link drive" style="background:#f3e8fd; color:#6f42c1; border-color:rgba(107,68,214,0.2)" href="BAN LAM VIEC 2.pdf" target="_blank" download>📄 Tải BAN LAM VIEC 2.pdf</a>'
html, count1 = re.subn(block_1_pattern, r'\g<1>' + block_1_inject, html, flags=re.DOTALL)

# 2. Inject for "Bài tập thực hành 2: Tủ trang trí 3 ngăn kéo 1 cánh mở"
block_2_pattern = r'(<div class="topic-title">\s*Bài tập thực hành 2: Tủ trang trí 3 ngăn kéo 1 cánh mở\s*</div>.*?<div class="resources">)'
block_2_inject = r'\n          <a class="chip-link drive" style="background:#f3e8fd; color:#6f42c1; border-color:rgba(107,68,214,0.2)" href="BAN VE TU TRANG TRI 3NK 1 C.pdf" target="_blank" download>📄 Tải BAN VE TU TRANG TRI 3NK 1 C.pdf</a>'
html, count2 = re.subn(block_2_pattern, r'\g<1>' + block_2_inject, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print(f"Updated Topic 1: {count1}, Topic 2: {count2}")
