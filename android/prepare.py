#!/usr/bin/env python3
"""Turns the web app (docs/app) into the Android app. Run from this folder.

  python3 prepare.py www               copy ../docs/app into www/ (no service worker or web manifest inside the app)
  python3 prepare.py native 0.1.0 7    after `npx cap add android`: icons, launch screen, camera, version
"""
import os, re, sys, shutil, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, '..', 'docs', 'app', 'icons')

def www():
    out = os.path.join(HERE, 'www'); shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(HERE, '..', 'docs', 'app'), out)
    p = os.path.join(out, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r"<script>if\('serviceWorker' in navigator\)[^<]*</script>\n?", '', s)
    s = re.sub(r'<link rel="manifest"[^>]*>', '', s)
    open(p, 'w', encoding='utf-8').write(s)
    for f in ['sw.js', 'manifest.webmanifest']:
        try: os.remove(os.path.join(out, f))
        except FileNotFoundError: pass
    print('www ready')

def native(version, code):
    from PIL import Image
    app = os.path.join(HERE, 'android', 'app'); res = os.path.join(app, 'src', 'main', 'res')
    full = Image.open(os.path.join(ICONS, 'icon-512.png')).convert('RGBA')
    mask = Image.open(os.path.join(ICONS, 'icon-maskable-512.png')).convert('RGBA')
    sizes = {'mdpi': (48, 108), 'hdpi': (72, 162), 'xhdpi': (96, 216), 'xxhdpi': (144, 324), 'xxxhdpi': (192, 432)}
    for d, (s, fg) in sizes.items():
        folder = os.path.join(res, 'mipmap-' + d); os.makedirs(folder, exist_ok=True)
        full.resize((s, s), Image.LANCZOS).save(os.path.join(folder, 'ic_launcher.png'))
        full.resize((s, s), Image.LANCZOS).save(os.path.join(folder, 'ic_launcher_round.png'))
        mask.resize((fg, fg), Image.LANCZOS).save(os.path.join(folder, 'ic_launcher_foreground.png'))
    open(os.path.join(res, 'values', 'ic_launcher_background.xml'), 'w').write(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#C38D9F</color>\n</resources>\n')
    # launch screen: the logo on sip.'s paper
    logo = full.crop((90, 120, 422, 400))
    for sp in glob.glob(os.path.join(res, 'drawable*', 'splash.png')):
        w, h = Image.open(sp).size; im = Image.new('RGBA', (w, h), (195, 141, 159, 255))
        s = int(min(w, h) * .42); lg = logo.resize((s, int(s * logo.height / logo.width)), Image.LANCZOS)
        im.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2)); im.convert('RGB').save(sp)
    # camera, for snapping drinks
    mp = os.path.join(app, 'src', 'main', 'AndroidManifest.xml'); m = open(mp).read()
    if 'android.permission.CAMERA' not in m:
        m = m.replace('<uses-permission android:name="android.permission.INTERNET" />',
            '<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.CAMERA" />\n    <uses-feature android:name="android.hardware.camera" android:required="false" />')
    open(mp, 'w').write(m)
    # version
    gp = os.path.join(app, 'build.gradle'); g = open(gp).read()
    v = version.lstrip('v') or '0.1.0'
    g = re.sub(r'versionCode \d+', 'versionCode ' + str(int(code)), g)
    g = re.sub(r'versionName "[^"]*"', 'versionName "' + v + '"', g)
    open(gp, 'w').write(g)
    print('native ready', v, code)

if __name__ == '__main__':
    if sys.argv[1] == 'www': www()
    else: native(sys.argv[2] if len(sys.argv) > 2 else '0.1.0', sys.argv[3] if len(sys.argv) > 3 else '1')
