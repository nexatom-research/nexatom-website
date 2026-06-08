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
        if '<main class="page">' not in text:
            fail(f"{html.relative_to(ROOT)} missing page wrapper")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    for phrase in [
        "Indigenous precision laser sources and scientific instruments",
        "Let's build together",
        "Explore UTT810",
        "Download Software",
        "Nexatom UTT810 Universal Time Tagger",
        "Problem and Solution",
        "A Closer Look",
        "Achievements",
        "Press Coverage",
        "Subodh Vashist",
        "nexatom.research@gmail.com",
    ]:
        if phrase not in home:
            fail(f"homepage missing phrase: {phrase}")

    product = (SITE / "products/utt810/index.html").read_text(encoding="utf-8")
    for phrase in [
        "Nexatom UTT810 Universal Time Tagger",
        "8 input channels",
        "1 ps time bin width",
        "&lt;10 ps",
        "4 ns dead time",
        "USB 3 data transfer",
        "Real-time FPGA",
        "External 10 MHz TTL",
        "minimum 8 ns bin width",
        "1 ps to 4 ns physical delay",
        "Use External Sync",
        "Quantum optics",
        "Spectroscopy",
        "Multi-channel event timing",
        "24.5 ps FWHM / 10.5 ps RMS",
    ]:
        if phrase not in product:
            fail(f"product page missing phrase: {phrase}")

    download = (SITE / "downloads/utt810/index.html").read_text(encoding="utf-8")
    for phrase in [
        "Nexatom UTT810 Time Tagger Software",
        "Download for Windows",
        "1.0.1",
        "85.78 MB",
        "cee5a78865e0b0923649c4f922327ab54de059721135fefa8bda499ed6510e3a",
        "After first install, future updates are available inside the app.",
        "https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.1/Nexatom_UTT810_Setup_1.0.1.exe",
        "https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json",
    ]:
        if phrase not in download:
            fail(f"download page missing phrase: {phrase}")

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
