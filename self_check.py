import json
import subprocess
import sys

r = subprocess.run(
    [
        sys.executable,
        'ai-agent-account-isolation-checker-20260803.py',
        'examples/profile-a',
        'examples/profile-b',
        '--json',
    ],
    capture_output=True,
    text=True,
)
assert r.returncode == 1, r.stdout
data = json.loads(r.stdout)
assert data['shared_secret_file_count'] == 1
assert data['credential_like_files'] == 2
assert data['files'][0]['entropy_bits_per_byte'] > 0
assert data['duplicates'][0]['entropy_bits_per_byte'] == data['files'][1]['entropy_bits_per_byte']
assert data['remediations'][0]['action'] == 'rotate-or-isolate-duplicate-secret'

r = subprocess.run(
    [
        sys.executable,
        'ai-agent-account-isolation-checker-20260803.py',
        'examples/profile-a',
        'examples/profile-b',
        '--min-entropy',
        '2',
    ],
    capture_output=True,
    text=True,
)
assert r.returncode == 1, r.stdout
assert 'high_entropy_file_count=2' in r.stdout

r = subprocess.run(
    [
        sys.executable,
        'ai-agent-account-isolation-checker-20260803.py',
        'examples/profile-a',
        'examples/profile-b',
        '--remediation',
    ],
    capture_output=True,
    text=True,
)
assert r.returncode == 1, r.stdout
assert '# Account isolation remediation plan' in r.stdout
assert 'Rotate the credential' in r.stdout
assert 'examples/profile-b' in r.stdout.replace('\\', '/')

print('self-check passed: detected shared credential-like file, entropy scores, and remediation plan')
