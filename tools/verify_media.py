"""Offline media regression checks: unique visuals, responsive paths and byte budgets."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from verify_growth import Page


def verify(base=""):
    root = Path(__file__).resolve().parents[1]
    site = root / "site"
    manifest = json.loads((root / "content/media/image-prompts.json").read_text(encoding="utf-8"))
    assert len(manifest["assets"]) == 18
    hashes = set()
    for asset in manifest["assets"]:
        for width, filename in zip((480, 960), asset["final_assets"]):
            data = (root / filename).read_bytes()
            assert len(data) < (65000 if width == 480 else 180000), filename + " over budget"
            if width == 960:
                hashes.add(hashlib.sha256(data).hexdigest())
    assert len(hashes) == 18, "Duplicate service/card images"
    service_images = set()
    for path in site.rglob("*.html"):
        source = path.read_text(encoding="utf-8")
        assert "hibuwebsites" not in source, str(path)
        page = Page(source)
        for tag, attrs in page.tags:
            urls = [attrs[k] for k in ("src", "poster", "data-video-mobile", "data-video-desktop") if k in attrs]
            urls += [c.strip().split()[0] for c in attrs.get("srcset", "").split(",") if c.strip()]
            for url in urls:
                if urlsplit(url).scheme or not url.startswith("/"):
                    continue
                assert url.startswith(base + "/"), f"{path}: wrong preview prefix: {url}"
                assert (site / url[len(base):].lstrip("/")).is_file(), f"Missing {url}"
            if tag == "img" and attrs.get("class") == "service-image":
                assert attrs.get("width") == "960" and attrs.get("height") == "720"
                assert attrs.get("loading") == "lazy" and attrs.get("alt")
                service_images.add(attrs["src"])
    assert len(service_images) == 12
    home = Page((site / "index.html").read_text(encoding="utf-8"))
    cards = [a for t, a in home.tags if t == "img" and a.get("class") == "svc-card__photo"]
    assert len(cards) == 6 and len({a["src"] for a in cards}) == 6
    assert not service_images.intersection(a["src"] for a in cards)
    videos = [a for t, a in home.tags if t == "video"]
    assert len(videos) == 1 and "src" not in videos[0] and videos[0]["preload"] == "none"
    assert not any("data-intro" in a for _, a in home.tags)
    assert not any("fonts.googleapis" in a.get("href", "") for _, a in home.tags)
    assert (site / "assets/video/austin-pennybacker-mobile.mp4").stat().st_size < 2000000
    assert (site / "assets/video/austin-pennybacker-desktop.mp4").stat().st_size < 5500000
    assert (site / "assets/images/austin-pennybacker-mobile.webp").stat().st_size < 100000
    assert (site / "assets/images/austin-pennybacker-1600.webp").stat().st_size < 250000
    print(f"PASS: 18 distinct images, 12 service pages, responsive media paths and byte budgets ({base or 'root'}).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="")
    verify(parser.parse_args().base)
