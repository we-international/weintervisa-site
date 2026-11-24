"""content/posts/<slug>.md -> Wix Blog Ricos JSON (headings, paragraphs, bullet lists, divider, bold/italic/links).

Usage: python3 tools/md_to_ricos.py content/posts/<slug>.md [out.json]
Used to publish a new post on the live Wix blog before the DNS day (skill wix-to-static-migration).
"""
import json,re,sys
src=open(sys.argv[1]).read()
meta=json.loads(re.search(r"<!--meta\n(.*?)\nmeta-->",src,re.S).group(1))
body=src.split("meta-->",1)[1].strip()
def inline(t):
    out=[];pos=0
    pat=re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*")
    for m in pat.finditer(t):
        if m.start()>pos: out.append((t[pos:m.start()],[]))
        if m.group(1): out.append((m.group(1),[{"type":"LINK","linkData":{"link":{"url":m.group(2),"target":"BLANK","rel":{"noreferrer":True}}}}]))
        elif m.group(3): out.append((m.group(3),[{"type":"BOLD","fontWeightValue":700}]))
        else: out.append((m.group(4),[{"type":"ITALIC","italicData":True}]))
        pos=m.end()
    if pos<len(t): out.append((t[pos:],[]))
    return [{"type":"TEXT","nodes":[],"textData":{"text":s,"decorations":d}} for s,d in out]
def para(t): return {"type":"PARAGRAPH","nodes":inline(t),"paragraphData":{}}
nodes=[];lst=None
for line in body.split("\n"):
    if line.startswith("- "):
        if lst is None: lst={"type":"BULLETED_LIST","nodes":[],"bulletedListData":{"indentation":0}}; nodes.append(lst)
        lst["nodes"].append({"type":"LIST_ITEM","nodes":[para(line[2:])]}); continue
    lst=None
    if not line.strip(): continue
    m=re.match(r"(#+) (.*)",line)
    if m: nodes.append({"type":"HEADING","nodes":inline(m.group(2)),"headingData":{"level":len(m.group(1))}})
    elif line.strip()=="---": nodes.append({"type":"DIVIDER","nodes":[],"dividerData":{"lineStyle":"SINGLE","width":"LARGE","alignment":"CENTER"}})
    else: nodes.append(para(line))
json.dump({"meta":meta,"richContent":{"nodes":nodes}},open(sys.argv[2] if len(sys.argv)>2 else "post.json","w"),ensure_ascii=False)
print(len(nodes), [n["type"] for n in nodes][:12])
