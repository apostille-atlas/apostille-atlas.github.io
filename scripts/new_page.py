#!/usr/bin/env python3
"""Scaffold tonight's page from the first unchecked backlog item.
Usage: python3 scripts/new_page.py            # scaffold next item
       python3 scripts/new_page.py --done     # mark the first unchecked item as published
New pages are created with "draft": true and are NOT built until you fill in facts + sources and remove draft."""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
BL = R / "backlog.md"
lines = BL.read_text().splitlines()
idx = next((i for i, l in enumerate(lines) if l.startswith("- [ ] ") and "(remaining" not in l), None)
if idx is None: sys.exit("Backlog empty: add ideas to backlog.md")
item = lines[idx][6:]
if "--done" in sys.argv:
    lines[idx] = lines[idx].replace("- [ ]", "- [x]", 1); BL.write_text("\n".join(lines) + "\n"); print("Marked done:", item); sys.exit()
kind, _, rest = item.partition(":"); name = re.split(r"[(—]", rest)[0].strip()
slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
if kind == "state":
    p = R / "data/states.json"; data = json.loads(p.read_text())
    if any(s["slug"] == slug for s in data): sys.exit(f"{slug} already exists")
    data.append({"slug": slug, "name": name, "abbr": "XX", "draft": True, "authority": "TODO", "fee": 0, "fee_note": "TODO",
                 "mail": True, "walk_in": False, "mail_time": "TODO (only if the office publishes it)", "walkin_time": "TODO",
                 "payment": "TODO", "addresses": ["TODO"], "phone": "", "what_to_send": ["TODO"], "tips": ["TODO"], "sources": [],
                 "summary": "TODO 2-3 sentence direct answer, official facts only", "last_reviewed": "TODO YYYY-MM-DD"})
    p.write_text(json.dumps(data, indent=1)); print(f"Added draft state '{name}' to data/states.json. Fill every TODO, add sources, delete \"draft\".")
else:
    if kind == "country": slug = "apostille-for-" + slug
    f = R / "content/guides" / f"{slug}.html"
    if f.exists(): sys.exit(f"{f} exists")
    meta = {"title": f"TODO title: {name}", "description": "TODO 150-char description", "h1": name, "category": kind.strip().title(), "draft": True, "sources": [],
            "summary": "TODO 2-3 sentence direct answer, official facts only",
            "faqs": [["TODO real question from research/questions.md", "TODO answer citing the official source"]], "last_reviewed": "TODO YYYY-MM-DD"}
    f.write_text(f"<!--{json.dumps(meta)}-->\n<p class=\"lede\">TODO</p>\n"); print("Created draft", f)
