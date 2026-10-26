#!/usr/bin/env python3
"""Submit all URLs from the live sitemap to IndexNow (free, no account)."""
import json, re, urllib.request
from pathlib import Path
R = Path(__file__).resolve().parent.parent
SITE = json.loads((R / "config.json").read_text())["site_url"].rstrip("/")
key = next((R / "static").glob("*.txt")).stem
sm = urllib.request.urlopen(SITE + "/sitemap.xml").read().decode()
urls = re.findall(r"<loc>(.*?)</loc>", sm)
body = json.dumps({"host": SITE.split("//")[1], "key": key, "keyLocation": f"{SITE}/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    r = urllib.request.urlopen(req); print("HTTP", r.status, r.read().decode()[:300])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:300])
print(len(urls), "URLs submitted")
