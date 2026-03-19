import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m1 = re.search(r'<div class="topic-title">(.*?01.*?)</div>', html, re.IGNORECASE)
if m1: print('Found Topic 1:', m1.group(1))

m2 = re.search(r'<div class="topic-title">(.*?trang trí.*?)</div>', html, re.IGNORECASE)
if m2: print('Found Topic 2:', m2.group(1))
