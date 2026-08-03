import argparse,hashlib,json,os,re
SECRET=re.compile(r'(api[_-]?key|token|secret|session|cookie)',re.I)
def digest(p):
 h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()
def main(argv=None):
 ap=argparse.ArgumentParser(description='Find shared credential-looking files across local AI agent account profiles.')
 ap.add_argument('roots',nargs='+'); ap.add_argument('--json',action='store_true'); ns=ap.parse_args(argv)
 seen={}; findings=[]
 for root in ns.roots:
  for dirpath,_,files in os.walk(root):
   for f in files:
    p=os.path.join(dirpath,f); rel=os.path.relpath(p,root)
    if SECRET.search(f) or SECRET.search(rel):
     try: h=digest(p)
     except OSError: continue
     if h in seen: findings.append({'hash':h[:12],'first':seen[h],'duplicate':p,'relative':rel})
     else: seen[h]=p
 out={'credential_like_files':len(seen)+len(findings),'shared_secret_file_count':len(findings),'duplicates':findings}
 print(json.dumps(out,indent=2) if ns.json else f"shared_secret_file_count={len(findings)}")
 return 1 if findings else 0
if __name__=='__main__': raise SystemExit(main())
