import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. "Bài tập thực hành 01 & 02" -> needs "BLV 1.pdf" and "BAN LAM VIEC 2.pdf"
# 2. "Bài tập thực hành 2: Tủ trang trí 3 ngăn kéo 1 cánh mở" -> needs "BAN VE TU TRANG TRI 3NK 1 C.pdf"

# Find the cards
cards = html.split('<div class="topic-card"')

def inject_links(card_content, pdfs):
    # Find the resources div and append the links inside it
    link_html = ''
    for pdf, title in pdfs:
        link_html += f'\n          <a class="chip-link drive" style="background:#f3e8fd; color:#6f42c1; border-color:rgba(107,68,214,0.2)" href="{pdf}" target="_blank" download>📄 Tải {title}</a>'
        
    # Inject just before the closing </div> of <div class="resources">
    # We can match r'<div class="resources">(.*?)</div>' with DOTALL and replace
    def repl(m):
        return f'<div class="resources">{m.group(1)}{link_html}\n        </div>'
        
    return re.sub(r'<div class="resources">(.*?)</div>', repl, card_content, flags=re.DOTALL)

new_html = cards[0]
updated = 0

for i in range(1, len(cards)):
    card = '<div class="topic-card"' + cards[i]
    m = re.search(r'<div class="topic-title">(.*?)</div>', card)
    if m:
        t = m.group(1).lower().strip()
        if 'bài tập thực hành 01' in t:
            card = inject_links(card, [('BLV 1.pdf', 'BLV 1.pdf'), ('BAN LAM VIEC 2.pdf', 'BAN LAM VIEC 2.pdf')])
            updated += 1
        elif 'tủ trang trí' in t:
            card = inject_links(card, [('BAN VE TU TRANG TRI 3NK 1 C.pdf', 'BAN VE TU TRANG TRI 3NK 1 C.pdf')])
            updated += 1
            
    new_html += card

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
    
print(f"Injected PDFs into {updated} topics.")
