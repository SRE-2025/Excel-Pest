#!/usr/bin/env python3
"""
Bundle the generated ./site into ONE self-contained, clickable HTML file.

Every page's body is stored in an in-page map; a tiny hash router swaps pages on
internal-link clicks and re-runs the site's own JS, so the full multi-page site
(with all motion/features) works from a single file with no server, no AWS, and
no GitHub. Output: preview/excel-pest-site-preview.html

    python3 tools/build.py && python3 tools/bundle_preview.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "preview", "excel-pest-site-preview.html")


def body_inner(htmltext):
    m = re.search(r"<body>(.*)</body>", htmltext, re.S)
    inner = m.group(1) if m else htmltext
    # Drop the per-page external script tags (we re-run the JS ourselves)
    inner = re.sub(r'<script src="/js/[^"]+"></script>', "", inner)
    return inner.strip()


def page_style(htmltext):
    """Pull any page-specific <style> from the head (e.g. pay-invoice)."""
    return "\n".join(re.findall(r"<style>(.*?)</style>", htmltext, re.S))


def route_key(rel):
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    return "/" + rel


def to_init(src, name):
    """Turn a `(function () { ... })();` IIFE into `function name() { ... }`."""
    src = src.replace("(function () {", "function %s() {" % name, 1)
    src = re.sub(r"\}\)\(\);\s*$", "}", src.strip())
    return src


def main():
    css = open(os.path.join(SITE, "css", "styles.css"), encoding="utf-8").read()
    main_js = to_init(open(os.path.join(SITE, "js", "main.js"), encoding="utf-8").read(), "initMain")
    inter_js = to_init(open(os.path.join(SITE, "js", "interactive.js"), encoding="utf-8").read(), "initInteractive")

    pages = {}
    extra_style = []
    for f in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(f, SITE)
        t = open(f, encoding="utf-8").read()
        pages[route_key(rel)] = body_inner(t)
        ps = page_style(t)
        if ps:
            extra_style.append(ps)

    shell = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Excel Pest — full site preview</title>
<style>
%s
%s
/* preview chrome */
#preview-note{position:fixed;z-index:200;left:50%%;bottom:14px;transform:translateX(-50%%);
  background:#071633;color:#fff;font:600 12px/1.4 system-ui,sans-serif;padding:8px 14px;border-radius:999px;
  box-shadow:0 8px 24px rgba(0,0,0,.3);opacity:.9}
#preview-note b{color:#f2a24d}
</style>
</head>
<body>
<div id="app"></div>
<div id="preview-note">Preview build · <b>click anything</b> — full site, all pages</div>
<script>
%s
%s
var PAGES = %s;
var app = document.getElementById('app');
function norm(p){ if(!p) return '/'; p = p.split('?')[0]; if(p==='/index.html') return '/'; return p; }
function render(p){
  p = norm(p);
  app.innerHTML = PAGES[p] || PAGES['/404.html'] || '<p style="padding:40px">Not found</p>';
  window.scrollTo(0,0);
  try { initMain(); } catch(e){}
  try { initInteractive(); } catch(e){}
}
document.addEventListener('click', function(e){
  var a = e.target.closest('a'); if(!a) return;
  var href = a.getAttribute('href') || '';
  if(href.charAt(0) === '/'){ e.preventDefault(); if(('#'+norm(href)) === location.hash){ render(norm(href)); } else { location.hash = norm(href); } }
});
window.addEventListener('hashchange', function(){ render(location.hash.slice(1)); });
render(location.hash.slice(1) || '/');
</script>
</body>
</html>
""" % (css, "\n".join(extra_style), main_js, inter_js, json.dumps(pages))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(shell)
    print("Wrote %s (%d pages, %.0f KB)" % (OUT, len(pages), os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
