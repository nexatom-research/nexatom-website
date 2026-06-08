from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    required = [
        "index.html",
        "products/index.html",
        "products/utt810/index.html",
        "downloads/index.html",
        "downloads/utt810/index.html",
        "achievements/index.html",
        "press/index.html",
        "team/index.html",
        "contact/index.html",
        "404.html",
        "robots.txt",
        "sitemap.xml",
        "CNAME",
        ".nojekyll",
        "assets/css/styles.css",
    ]
    for rel in required:
        if not (SITE / rel).exists():
            fail(f"missing site/{rel}")

    html_files = sorted(SITE.rglob("*.html"))
    for html in html_files:
        text = html.read_text(encoding="utf-8")
        if '<link rel="stylesheet" href="/assets/css/styles.css">' not in text:
            fail(f"{html.relative_to(ROOT)} must load /assets/css/styles.css")
        if 'href="products/' in text or 'href="downloads/' in text:
            fail(f"{html.relative_to(ROOT)} contains depth-sensitive relative nav links")
        if 'ghs.googlehosted.com' in text or 'drive.google.com' in text:
            fail(f"{html.relative_to(ROOT)} contains old Google-hosted download/media link")
        if '<header class="site-header">' not in text:
            fail(f"{html.relative_to(ROOT)} missing shared header")
        if '<footer class="site-footer">' not in text:
            fail(f"{html.relative_to(ROOT)} missing shared footer")

    cname = (SITE / "CNAME").read_text(encoding="utf-8").strip()
    if cname != "www.nexatom.in":
        fail("site/CNAME must contain www.nexatom.in")

    forbidden = [
        SITE / "docs",
        SITE / "mockups",
        SITE / ".superpowers",
        SITE / "time_tagger_precision_detail_specification.pdf",
        SITE / "Nexatom_TT_Specifications (1).pdf",
    ]
    for path in forbidden:
        if path.exists():
            fail(f"forbidden public artifact exists: {path.relative_to(ROOT)}")

    print("OK: site skeleton verified")


if __name__ == "__main__":
    main()
