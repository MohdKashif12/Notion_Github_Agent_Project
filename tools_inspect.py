# Quick helper to inspect a file's raw bytes and text
p = r"c:\Users\HP\Desktop\notion_git_agent\main_agent.py"
with open(p, 'rb') as f:
    b = f.read()
print('LENGTH_BYTES:', len(b))
# Show first 1000 bytes, safe repr
print(repr(b[:1000]))
# Also print as utf-8 decoded with replacement for visibility
print('DECODED (first 1000 chars):')
print(b[:1000].decode('utf-8', errors='replace'))
