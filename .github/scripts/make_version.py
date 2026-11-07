#!/usr/bin/env python3
"""Writes fonts/version.json: { "build": N, "fonts": { "<name>": "<first 12 hex of the sha256 of fonts/<name>.ttf>" } }, one entry per font (the TTFs of fonts/; the woff2 files and slices of a font follow its TTF).
Prints "<build> <names of the fonts that changed>" to stdout; exits 3 when no font changed (no new version)."""
import hashlib, json, os, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'fonts'))
fonts = {}
for n in sorted(os.listdir('.')):
    if n.endswith('.ttf'):
        h = hashlib.sha256()
        with open(n, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
        fonts[n[:-4]] = h.hexdigest()[:12]
old = json.load(open('version.json')) if os.path.exists('version.json') else {}
was = old.get('fonts', {})
changed = sorted(n for n in set(fonts) | set(was) if fonts.get(n) != was.get(n))
if old and not changed: sys.exit(3)
build = old.get('build', 0) + 1
with open('version.json', 'w') as f: json.dump({'build': build, 'fonts': fonts}, f, indent=1); f.write('\n')
print(build, *changed)
