#!/usr/bin/env python3
"""Writes fonts/version.json: the state of every file in fonts/ (sha256, size) and what changed since the last version.json.
Prints the release notes to the file given with --notes and the build number to stdout; exits 3 when nothing changed (no new version).
{ build, time, commit, files: { "migoi.ttf": { sha256, size } }, changes: { added, changed, removed }, log: ["<sha> <subject>"] }"""
import argparse, hashlib, json, os, subprocess, sys, datetime

ap = argparse.ArgumentParser()
ap.add_argument('--notes', default='')
a = ap.parse_args()
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
os.chdir(root)
FONTS, OUT = 'fonts', 'fonts/version.json'
git = lambda *c: subprocess.run(['git', *c], capture_output=True, text=True).stdout.strip()

files = {}
for d, _, names in os.walk(FONTS):
    for n in names:
        p = os.path.join(d, n).replace(os.sep, '/')
        if p == OUT: continue
        h = hashlib.sha256()
        with open(p, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
        files[p[len(FONTS) + 1:]] = {'sha256': h.hexdigest(), 'size': os.path.getsize(p)}
files = dict(sorted(files.items()))

old = {}
if os.path.exists(OUT):
    with open(OUT) as f: old = json.load(f)
was = old.get('files', {})
changes = {'added': sorted(set(files) - set(was)),
           'changed': sorted(n for n in files if n in was and files[n]['sha256'] != was[n]['sha256']),
           'removed': sorted(set(was) - set(files))}
if old and not any(changes.values()):
    print('no change', file=sys.stderr); sys.exit(3)

build = old.get('build', 0) + 1
head = git('rev-parse', 'HEAD')
since = old.get('commit')
log = git('log', '--pretty=%h %s', f'{since}..HEAD', '--', FONTS).splitlines() if since and git('cat-file', '-t', since) == 'commit' else git('log', '-20', '--pretty=%h %s', '--', FONTS).splitlines()
version = {'build': build, 'time': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'commit': head, 'files': files, 'changes': changes, 'log': log}
with open(OUT, 'w') as f: json.dump(version, f, indent=1, ensure_ascii=False); f.write('\n')

if a.notes:
    lines = [f'Fonts, build {build}', '']
    for k, t in (('added', 'New'), ('changed', 'Changed'), ('removed', 'Removed')):
        if changes[k]: lines += [f'**{t}** ({len(changes[k])}):'] + [f'- `{n}`' for n in changes[k]] + ['']
    if log: lines += ['**Commits**:'] + [f'- {l}' for l in log]
    with open(a.notes, 'w') as f: f.write('\n'.join(lines) + '\n')
print(build)
