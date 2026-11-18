#!/usr/bin/env python3
"""Copy every Wix-hosted image (static.wixstatic.com) used by the posts into assets/img/
and point the content at the local copy, so the site no longer depends on Wix after the
Wix plan ends. Run once on a machine/CI runner that can reach static.wixstatic.com:

    python3 tools/fetch_images.py && python3 tests/test_site.py
"""
import re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"
IMG.mkdir(parents=True, exist_ok=True)
pat = re.compile(r"https://static\.wixstatic\.com/media/([\w~.-]+\.(?:jpe?g|png|webp|gif))", re.I)

done = 0
for f in (ROOT / "content/posts").glob("*.md"):
    s = f.read_text()
    for url, name in set((m.group(0), m.group(1)) for m in pat.finditer(s)):
        local = IMG / name.replace("~", "-")
        if not local.exists():
            with urllib.request.urlopen(url, timeout=60) as r:
                local.write_bytes(r.read())
            done += 1
        s = s.replace(url, "/assets/img/" + local.name)
    f.write_text(s)
print(f"downloaded {done} images into {IMG}")
