import subprocess,sys,json
r=subprocess.run([sys.executable,'ai-agent-account-isolation-checker-20260803.py','examples/profile-a','examples/profile-b','--json'],capture_output=True,text=True)
assert r.returncode==1
data=json.loads(r.stdout); assert data['shared_secret_file_count']==1
print('self-check passed: detected shared credential-like file across profiles')
