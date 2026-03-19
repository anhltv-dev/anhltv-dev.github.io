import re

with open('index.html', 'r', encoding='utf-8') as f:
    hc = f.read()

# Replace <iframe src="URL"></iframe> with:
# <iframe data-src="URL" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" allowfullscreen></iframe>
def replacer(match):
    original_tags = match.group(0)
    # Extract src
    src_match = re.search(r'src="([^"]+)"', original_tags)
    if not src_match:
        return original_tags
    
    src = src_match.group(1)
    
    # If it already has data-src, leave it
    if 'data-src=' in original_tags:
        return original_tags
        
    # Build new iframe
    # Replace src="X" with data-src="X" src="base64"
    new_tags = original_tags.replace(f'src="{src}"', f'data-src="{src}" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="')
    # Also add allowfullscreen if missing
    if 'allowfullscreen' not in new_tags:
        new_tags = new_tags.replace('>', ' allowfullscreen>', 1)
        
    return new_tags

hc = re.sub(r'<iframe.*?>', replacer, hc)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(hc)

print("Done replacing iframes.")
