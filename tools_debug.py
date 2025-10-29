import io
import sys
from pathlib import Path

p = Path(r"c:\Users\HP\Desktop\notion_git_agent\notion_connector.py")
print('FILE:', p)
data = p.read_bytes()
print('LENGTH_BYTES:', len(data))
print('PREFIX_BYTES_REPR:')
print(repr(data[:1000]))
print('\nDECODED (utf-8, errors=replace):')
print(data.decode('utf-8', errors='replace')[:2000])

print('\n--- AST PARSE ---')
import ast
try:
    tree = ast.parse(data)
    names = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    assigns = [n.targets[0].id for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)]
    print('Top-level defs (functions/classes):', names)
    print('Top-level assigned names:', assigns)
except Exception as e:
    print('AST parse error:', e)

print('\n--- EXECUTE IN FRESH NAMESPACE ---')
ns = {}
try:
    exec(compile(data, str(p), 'exec'), ns)
    public = [k for k in ns.keys() if not k.startswith('__')]
    print('EXECUTION OK, public names:', public)
    # If search_notion exists, print its repr
    if 'search_notion' in ns:
        print('search_notion repr:', repr(ns['search_notion']))
except Exception as e:
    print('EXECUTION RAISED:', type(e).__name__, e)
    import traceback
    traceback.print_exc()

print('\n--- DONE ---')
