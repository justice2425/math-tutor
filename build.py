#!/usr/bin/env python3
"""Build Math Tutor's single-file index.html from src/.

    python3 build.py           -> index.html       (release: test hook removed)
    python3 build.py --test    -> index.test.html  (keeps the window.__SNMT_TEST__ hook)
    python3 build.py --check   -> verifies index.html's CSP hash matches its script

The page's Content-Security-Policy only allows the one inline script whose
SHA-256 hash is listed in the <meta> tag. Any edit to src/app.js changes that
hash, so always rebuild with this script instead of editing index.html by hand.
Only the Python standard library is needed.
"""
import base64
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
HOOK = re.compile(r"/\* @test-hook-begin \*/.*?/\* @test-hook-end \*/", re.S)
CSP_HASH = re.compile(r"script-src 'sha256-[A-Za-z0-9+/=]+'")


def sha256_b64(text):
    return base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode()


def build(test=False):
    js = (SRC / "app.js").read_text(encoding="utf-8")
    if not test:
        js, n = HOOK.subn("", js)
        if n != 1:
            sys.exit(f"expected exactly one test-hook block, found {n}")
        if "__SNMT_TEST__" in js:
            sys.exit("test hook still present in release build")
    if "</script" in js.lower():
        sys.exit("app.js must not contain '</script' (it would end the inline script early)")
    head = (SRC / "head.html").read_text(encoding="utf-8")
    tail = (SRC / "tail.html").read_text(encoding="utf-8")
    head, n = CSP_HASH.subn(f"script-src 'sha256-{sha256_b64(js)}'", head)
    if n != 1:
        sys.exit(f"expected one script-src hash in head.html, found {n}")
    out = ROOT / ("index.test.html" if test else "index.html")
    out.write_text(head + "<script>" + js + "</script>" + tail, encoding="utf-8")
    print(f"wrote {out.name} ({out.stat().st_size:,} bytes)")
    return out


def check(path):
    html = path.read_text(encoding="utf-8")
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    listed = re.findall(r"script-src 'sha256-([A-Za-z0-9+/=]+)'", html)
    ok = len(scripts) == 1 and len(listed) == 1 and sha256_b64(scripts[0]) == listed[0]
    print(f"{path.name}: CSP hash {'matches' if ok else 'DOES NOT match'} the inline script")
    return ok


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if check(ROOT / "index.html") else 1)
    check(build(test="--test" in sys.argv))
