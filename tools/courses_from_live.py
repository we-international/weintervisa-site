"""Turn the live Wix /courses catalogue into content/courses.json (run by hand, read-only).

Input: review/compare-<run>/text/courses.inline.js.txt — the inline scripts of the live /courses embed,
saved as data by the workflow "Live Wix vs new site" (never run). We parse the JSON literals
`const courses = [...]`, `const topics = {...}`, `const images = {...}` and `const comparisonOptions = [...]`.

Provider names are NOT copied (owner rule 26 Oct 2026: course listings stay neutral and let the student
choose between colleges); only the number of partner-college options per course is kept.

Usage: python3 tools/courses_from_live.py <path to courses.inline.js.txt>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALTS = {"care": "Care worker supporting an older person", "health": "Healthcare students practising in a simulation room",
        "child": "Early childhood educator with children", "classroom": "International students studying together in a classroom",
        "city": "Students in an Australian city", "business": "Business students working together",
        "cookery": "Cookery students in a commercial kitchen", "trades": "Trades student on a building site"}


def grab(src, name):
    i = src.index(f"const {name}")
    j = src.index("=", i) + 1
    while src[j].isspace():
        j += 1
    open_, close = src[j], "]" if src[j] == "[" else "}"
    depth, k, q = 0, j, None
    while k < len(src):
        c = src[k]
        if q:
            if c == "\\":
                k += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == open_:
            depth += 1
        elif c == close:
            depth -= 1
            if not depth:
                break
        k += 1
    return json.loads(src[j:k + 1])


def main(path):
    src = Path(path).read_text()
    courses, topics, images, options = (grab(src, n) for n in ("courses", "topics", "images", "comparisonOptions"))
    count = {}
    for o in options:
        count[o["course"]] = count.get(o["course"], 0) + 1
    keep = ("id", "code", "title", "topic", "cities", "duration", "focus", "campuses", "studyNote")
    out_courses = []
    for c in courses:
        row = {k: c[k] for k in keep if c.get(k)}
        row["options"] = count.get(c["id"], 0)
        out_courses.append(row)
    out_topics = {k: {"group": t["group"], "image": t.get("image"),
                      **{f: (t.get(f) or [""])[0] for f in ("about", "skills", "suit", "use", "jobs")}}
                  for k, t in topics.items()}
    out_images = {}
    for k, url in images.items():
        m = re.search(r"/media/([^/~]+)~mv2\.(\w+)", url)
        out_images[k] = {"wix": url, "file": f"{m.group(1)}-mv2.webp", "alt": ALTS.get(k, "Study in Australia") + " (illustrative image)"}
    doc = {
        "_source": f"Live page www.weintervisa.com/courses (Wix custom embed): course data read from the embed's inline "
                   f"script saved by the workflow 'Live Wix vs new site' ({'review/compare-' + next((p.split('-')[-1] for p in Path(path).parts if p.split('-')[-1].isdigit() and len(p.split('-')[-1]) > 8), '?')}). "
                   "Provider names left out on purpose (neutral listing).",
        "courses": out_courses, "topics": out_topics, "images": out_images,
    }
    (ROOT / "content/courses.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(out_courses)} courses, {len(out_topics)} topics, {len(out_images)} images → content/courses.json")


if __name__ == "__main__":
    main(sys.argv[1])
