import os, json, pathlib, time, re
from slugify import slugify
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE = "https://surucoach.be"          # <-- your portal
AUTH = ("aBAyUrZhv8hCTS5eMK7HUtv1FwGVv5", "") # export TLMS_API_KEY=xxxxx before running
OUT  = pathlib.Path("talentlms_dump")
OUT.mkdir(exist_ok=True)

def get(path):
    r = requests.get(f"{BASE}{path}", auth=AUTH, timeout=20)
    r.raise_for_status()
    return r

# 1) courses list --------------------------------------------------------------
courses = get("/api/v1/courses").json()

for c in tqdm(courses, desc="courses"):
    cid, cname = c["id"], c["name"]
    cdir = OUT / f"{cid:04d}-{slugify(cname)}"
    cdir.mkdir(exist_ok=True)

    # 2) per-course detail -----------------------------------------------------
    course = get(f"/api/v1/courses/id:{cid}").json()
    (cdir / "course.json").write_text(json.dumps(course, indent=2))

    for u in course.get("units", []):
        if "url" not in u:            # e.g. Sections, ILT containers
            continue
        unit_html = get(f"/{u['url']}").text

        # (optional) clean up navigation header/footer so pages are truly standalone
        soup = BeautifulSoup(unit_html, "lxml")
        for tag in soup.select("header, nav, footer, script[src*=google]"):
            tag.decompose()

        fname = f"{u['id']:04d}-{slugify(u['name'])}.html"
        (cdir / fname).write_text(str(soup), encoding="utf-8")
        time.sleep(0.2)               # be polite to API
print("✔ All done. Files in", OUT.resolve()) 