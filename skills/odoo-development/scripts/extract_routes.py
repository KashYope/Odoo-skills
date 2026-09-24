#!/usr/bin/env python3
"""Static route declaration index. Never claims to resolve the runtime routing map."""
import argparse
import ast
import json
from pathlib import Path
from collections import Counter

def expr(node):
    return ast.unparse(node)

def literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        return {'expression': expr(node)}

def domain(module, paths):
    s = ' '.join(str(p) for p in paths)
    if module.startswith('auth_') or '/web/login' in s: return 'authentication'
    if '/web/session' in s: return 'session'
    if '/web/dataset' in s: return 'datasets-orm'
    if module == 'rpc' or '/jsonrpc' in s or '/xmlrpc' in s: return 'rpc-public-api'
    if '/report' in s: return 'reporting'
    if '/web/export' in s or module == 'base_import': return 'import-export'
    if '/web/action' in s: return 'actions'
    if module.startswith('website_sale'): return 'ecommerce'
    if module.startswith('payment'): return 'payments'
    if module == 'portal' or '/my/' in s: return 'portal'
    if module.startswith('mail'): return 'messaging'
    if module == 'bus': return 'notifications'
    if any(x in s for x in ['/web/content', '/web/image', '/web/binary', 'attachment']): return 'files-attachments'
    if module.startswith('website'): return 'website'
    if module == 'web': return 'web-client'
    return 'other:' + module

def extract(root, version, sha):
    rows, errors = [], []
    for p in sorted(root.rglob('*.py')):
        rel = p.relative_to(root).as_posix()
        if not (rel.startswith('odoo/') or rel.startswith('addons/')): continue
        source = p.read_text(encoding='utf-8')
        if 'route' not in source: continue
        try: tree = ast.parse(source)
        except SyntaxError as e:
            errors.append({'path': rel, 'error': str(e)}); continue
        aliases = {'route'}
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module in ('odoo.http', 'odoo'):
                aliases.update(a.asname or a.name for a in n.names if a.name == 'route')
        parts = rel.split('/')
        module = parts[parts.index('addons') + 1] if 'addons' in parts else 'framework'
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        for cls in classes:
            for fun in cls.body:
                if not isinstance(fun, (ast.FunctionDef, ast.AsyncFunctionDef)): continue
                for dec in fun.decorator_list:
                    if not isinstance(dec, ast.Call): continue
                    is_route = (isinstance(dec.func, ast.Attribute) and dec.func.attr == 'route') or (isinstance(dec.func, ast.Name) and dec.func.id in aliases)
                    if not is_route: continue
                    kw = {k.arg or '**': literal(k.value) for k in dec.keywords}
                    val = literal(dec.args[0]) if dec.args else kw.pop('route', [])
                    paths = val if isinstance(val, list) else [val]
                    nodes = list(ast.walk(fun))
                    calls = sorted({expr(n.func) for n in nodes if isinstance(n, ast.Call)})
                    models = sorted({n.slice.value for n in nodes if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Attribute) and n.value.attr == 'env' and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str)})
                    security = [c for c in calls if any(x in c for x in ['access', 'sudo', 'token', 'auth', 'check', 'sign', 'captcha'])]
                    rows.append({'version': version, 'sha': sha, 'module': module, 'file': rel,
                        'line': dec.lineno, 'end_line': fun.end_lineno, 'controller': cls.name,
                        'bases': [expr(b) for b in cls.bases], 'handler': fun.name,
                        'routes_declared': paths, 'routing_declared': kw,
                        'inheritance': 'republication-or-override' if not paths else 'declaration-may-also-override',
                        'effective_routing': 'UNRESOLVED: installed modules, controller MRO and dispatcher required',
                        'signature': expr(fun.args), 'backend_calls': calls, 'literal_models': models,
                        'security_call_candidates': security,
                        'return_expressions': [expr(n.value) if n.value else 'None' for n in nodes if isinstance(n, ast.Return)],
                        'domain': domain(module, paths),
                        'test_only_candidate': module.startswith('test_') or '/tests/' in rel or fun.name in ('unit_tests_suite', 'test_suite'),
                        'source_url': f'https://github.com/odoo/odoo/blob/{sha}/{rel}#L{dec.lineno}'})
    return rows, errors

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path); ap.add_argument('--version', required=True)
    ap.add_argument('--sha', required=True); ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args(); rows, errors = extract(a.root, a.version, a.sha)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    summary = {'version': a.version, 'sha': a.sha, 'declarations': len(rows),
        'literal_paths': sum(sum(isinstance(p, str) for p in r['routes_declared']) for r in rows),
        'domains': dict(Counter(r['domain'] for r in rows)), 'parse_errors': errors,
        'scope': 'Only files present in the supplied root; no runtime resolution; nested-call evidence is lexical.'}
    a.out.with_suffix('.summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False))
    if errors: raise SystemExit(2)

if __name__ == '__main__': main()
