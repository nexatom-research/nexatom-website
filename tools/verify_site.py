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
