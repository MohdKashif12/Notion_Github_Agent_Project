from pathlib import Path
p = Path(r"c:\Users\HP\Desktop\notion_git_agent")
for f in ['git_connector.py','reasoning_engine.py','main_agent.py','notion_connector.py']:
    fp = p / f
    print(f, 'exists', fp.exists(), 'size', fp.stat().st_size if fp.exists() else 'N/A')
    if fp.exists():
        print('--- repr prefix ---')
        print(repr(fp.read_bytes()[:400]))
        print('--- decoded prefix ---')
        try:
            print(fp.read_text(encoding='utf-8')[:800])
        except Exception as e:
            print('decode error', e)
    print('\n')
