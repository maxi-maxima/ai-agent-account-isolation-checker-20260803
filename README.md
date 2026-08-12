# AI Agent Account Isolation Checker

## Pain solved
Developers switch among multiple AI agent accounts and profiles. Accidentally reusing token/session files defeats isolation and can leak work identities.

## Why now
CLI coding agents and account switchers are trending, making local profile hygiene important.

## Install / run
Requires Python 3.9+. No third-party packages.

```bash
python ai-agent-account-isolation-checker-20260803.py --help
python ai-agent-account-isolation-checker-20260803.py examples/profile-a examples/profile-b --json
python ai-agent-account-isolation-checker-20260803.py examples/profile-a examples/profile-b --min-entropy 2
python self_check.py
```

## Entropy scoring
JSON output now includes each credential-like file's `entropy_bits_per_byte` and `high_entropy` flag. Use `--min-entropy` to tune the threshold for short local tokens or longer generated secrets.

## Example
See `examples/` for input files and expected output.

## Roadmap
- Windows/macOS known profile presets
- Remediation script generation

## License
MIT
