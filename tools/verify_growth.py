"""Offline regression checks for generated SEO/content. Run after build.py."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.text = []
        self.title = ""
        self.schema = []
        self.in_title = False
        self.in_schema = False
        self.schema_text = ""
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "title":
            self.in_title = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_schema = True
            self.schema_text = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_schema:
            self.schema.append(json.loads(self.schema_text))
            self.in_schema = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_title:
            self.title += data
        if self.in_schema:
            self.schema_text += data


def verify(base=""):
    site = Path(__file__).resolve().parents[1] / "site"
    pages = {p.relative_to(site).as_posix(): Page(p.read_text(encoding="utf-8")) for p in site.rglob("*.html")}
    errors = []
    titles, descriptions = [], []
    for path, page in pages.items():
        redirect = any(t == "meta" and a.get("http-equiv") == "refresh" for t, a in page.tags)
        if not redirect:
            if any(key in json.dumps(page.schema) for key in ('"aggregateRating"', '"reviewRating"')):
                errors.append(f"{path}: self-serving rating markup")
            if sum(t == "h1" for t, _ in page.tags) != 1:
                errors.append(f"{path}: expected one h1")
            titles.append(page.title)
            desc = [a.get("content", "") for t, a in page.tags if t == "meta" and a.get("name") == "description"]
            if len(desc) != 1 or not desc[0]:
                errors.append(f"{path}: missing description")
            else:
                descriptions.append(desc[0])
            expected = "https://www.excelpest-lawncontrol.com/" + ("" if path == "index.html" else path)
            canonical = [a.get("href") for t, a in page.tags if t == "link" and a.get("rel") == "canonical"]
            if canonical != [expected]:
                errors.append(f"{path}: incorrect canonical {canonical}")
        for tag, attrs in page.tags:
            field = "href" if tag in ("a", "link") else "src" if tag in ("img", "script") else None
            url = attrs.get(field, "") if field else ""
            parsed = urlsplit(url)
            if not url or parsed.scheme or parsed.netloc:
                continue
            local = unquote(parsed.path)
            if local.startswith("/"):
                if base and not local.startswith(base + "/"):
                    errors.append(f"{path}: missing preview prefix: {url}")
                    continue
                target = local[len(base):].lstrip("/") or "index.html"
            elif local:
                target = (Path(path).parent / local).as_posix()
            else:
                target = path
            if not (site / target).is_file():
                errors.append(f"{path}: broken local URL: {url}")
            if parsed.fragment and target in pages:
                ids = {a.get("id") for _, a in pages[target].tags}
                if unquote(parsed.fragment) not in ids:
                    errors.append(f"{path}: missing anchor: {url}")
    for label, values in (("title", titles), ("description", descriptions)):
        errors.extend(f"Duplicate {label}: {v}" for v, count in Counter(values).items() if count > 1)

    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap = ET.parse(site / "sitemap.xml")
    urls = [e.text for e in sitemap.findall("s:url/s:loc", ns)]
    for url in urls:
        path = urlsplit(url).path.lstrip("/") or "index.html"
        if path not in pages:
            errors.append("Sitemap missing file: " + path)
        elif any(t == "meta" and a.get("name") == "robots" and "noindex" in a.get("content", "") for t, a in pages[path].tags):
            errors.append("Noindex URL in sitemap: " + path)
    for expected in ("pest-library.html", "insights/central-texas-pest-calendar.html", "insights/fire-ants-central-texas-yard.html", "insights/cockroaches-central-texas-kitchen.html"):
        if not any(u.endswith("/" + expected) for u in urls):
            errors.append("New page absent from sitemap: " + expected)
    library = " ".join(pages["pest-library.html"].text).lower()
    for prohibited in ("armadillo", "skunk", "feral cat", "bat removal", "snake removal", "termite treatment"):
        if prohibited in library:
            errors.append("Off-menu library content: " + prohibited)
    for path, page in pages.items():
        if path.startswith("services/"):
            cities = {a.get("href") for t, a in page.tags if t == "a" and "/locations/" in a.get("href", "")}
            if len(cities) < 5:
                errors.append("Missing service-to-city links: " + path)
            if not any("service-side-media" in a.get("class", "") for _, a in page.tags):
                errors.append("Missing service sidebar: " + path)
            if "What affects the price?" not in " ".join(page.text):
                errors.append("Missing estimate guidance: " + path)
    termite = " ".join(pages["insights/termite-season-central-texas.html"].text)
    if "does not currently advertise termite" not in termite:
        errors.append("Termite guide must explain service limitation")
    if errors:
        raise SystemExit("\n".join(errors))
    rules = json.loads((site.parent / "infra/amplify-redirects.json").read_text())
    for rule in rules:
        target = rule["target"].lstrip("/") or "index.html"
        assert (site / target).is_file(), "Missing redirect target: " + target
    print(f"PASS: {len(pages)} HTML pages; {len(urls)} sitemap URLs; unique metadata, valid JSON-LD, local links, anchors and service scope ({base or 'root'}).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="")
    verify(parser.parse_args().base.rstrip("/"))
