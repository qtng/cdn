#!/usr/bin/env python3
"""Writes fonts/version.json: { "build": N, "fonts": { "<name>": "<UTC date and time of the last commit that changed fonts/<name>.ttf>" } }, one entry per font (the TTFs of fonts/; the woff2 files and slices of a font follow its TTF).
Needs the whole history (the dates come from git). Prints "<build> <names of the fonts that changed>" to stdout; exits 3 when no font changed (no new version)."""
import json, os, subprocess, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'fonts'))
env = dict(os.environ, TZ='UTC')
fonts = {}
for n in sorted(os.listdir('.')):
    if n.endswith('.ttf'):
        d = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=format-local:%Y-%m-%d %H:%M', '--', n], capture_output=True, text=True, env=env).stdout.strip()
        fonts[n[:-4]] = d
old = json.load(open('version.json')) if os.path.exists('version.json') else {}
was = old.get('fonts', {})
changed = sorted(n for n in set(fonts) | set(was) if fonts.get(n) != was.get(n))
if old and not changed: sys.exit(3)
build = old.get('build', 0) + 1
with open('version.json', 'w') as f: json.dump({'build': build, 'fonts': fonts}, f, indent=1); f.write('\n')
print(build, *changed)
