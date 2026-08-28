import argparse
import hashlib
import json
import math
import os
import re

SECRET = re.compile(r'(api[_-]?key|token|secret|session|cookie)', re.I)


def read_bytes(path):
    with open(path, 'rb') as fh:
        return fh.read()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def entropy_bits_per_byte(data):
    if not data:
        return 0.0
    counts = {}
    for byte in data:
        counts[byte] = counts.get(byte, 0) + 1
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return round(entropy, 3)


def looks_secret(path, root):
    rel = os.path.relpath(path, root)
    return SECRET.search(os.path.basename(path)) or SECRET.search(rel)


def scan_roots(roots, min_entropy):
    seen = {}
    findings = []
    files = []
    for root in roots:
        for dirpath, _, names in os.walk(root):
            for name in names:
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, root)
                if not looks_secret(path, root):
                    continue
                try:
                    data = read_bytes(path)
                except OSError:
                    continue
                sha = digest(data)
                entropy = entropy_bits_per_byte(data)
                item = {
                    'path': path,
                    'relative': rel,
                    'hash': sha[:12],
                    'entropy_bits_per_byte': entropy,
                    'high_entropy': entropy >= min_entropy,
                }
                files.append(item)
                if sha in seen:
                    findings.append({
                        'hash': sha[:12],
                        'first': seen[sha]['path'],
                        'duplicate': path,
                        'relative': rel,
                        'entropy_bits_per_byte': entropy,
                    })
                else:
                    seen[sha] = item
    remediations = []
    for finding in findings:
        remediations.append({
            'action': 'rotate-or-isolate-duplicate-secret',
            'duplicate': finding['duplicate'],
            'first': finding['first'],
            'reason': 'same credential-like file content appears in multiple profile roots',
        })
    return {
        'credential_like_files': len(files),
        'shared_secret_file_count': len(findings),
        'high_entropy_file_count': sum(1 for item in files if item['high_entropy']),
        'duplicates': findings,
        'remediations': remediations,
        'files': files,
    }


def render_remediation(out):
    lines = [
        '# Account isolation remediation plan',
        '',
        'Review each duplicate before changing files. Rotate exposed credentials before deleting local copies.',
    ]
    if not out['remediations']:
        lines.append('')
        lines.append('No duplicate credential-like files were found.')
        return '\n'.join(lines)
    for i, item in enumerate(out['remediations'], 1):
        lines.extend([
            '',
            f"## {i}. {item['action']}",
            f"- duplicate: {item['duplicate']}",
            f"- first_seen: {item['first']}",
            f"- reason: {item['reason']}",
            '- suggested_steps:',
            '  1. Confirm which profile should own this credential.',
            '  2. Rotate the credential with the provider if it may have crossed account boundaries.',
            '  3. Remove or replace the duplicate file after backup and re-run this checker.',
        ])
    return '\n'.join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Find shared credential-looking files across local AI agent account profiles.')
    ap.add_argument('roots', nargs='+')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--remediation', action='store_true', help='Emit a reviewable remediation plan for duplicate credential files')
    ap.add_argument('--min-entropy', type=float, default=4.0, help='Bits-per-byte threshold for high-entropy credential candidates')
    ns = ap.parse_args(argv)

    out = scan_roots(ns.roots, ns.min_entropy)
    if ns.json:
        print(json.dumps(out, indent=2))
    elif ns.remediation:
        print(render_remediation(out))
    else:
        print(
            f"shared_secret_file_count={out['shared_secret_file_count']} "
            f"high_entropy_file_count={out['high_entropy_file_count']}"
        )
    return 1 if out['shared_secret_file_count'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
