#!/usr/bin/env python3
"""Query the static Odoo route index; outputs declaration evidence, not effective ACLs."""
import argparse, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('index',type=Path); p.add_argument('--query',default='')
    p.add_argument('--module'); p.add_argument('--domain'); p.add_argument('--limit',type=int,default=20)
    a=p.parse_args(); matches=[]
    for line in a.index.read_text().splitlines():
        r=json.loads(line)
        if a.module and r['module']!=a.module: continue
        if a.domain and r['domain']!=a.domain: continue
        if not all(w.casefold() in json.dumps(r,ensure_ascii=False).casefold() for w in a.query.split()): continue
        matches.append(r)
    print(json.dumps({'total_matches':len(matches),'shown':min(len(matches),max(0,a.limit)),
        'warning':'Static declarations. Read parents, helpers and installed modules before reuse.',
        'results':matches[:max(0,a.limit)]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
