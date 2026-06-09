from pathlib import Path
from html.parser import HTMLParser
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.links.append((name, value))


def internal_target_exists(html: Path, url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith("/"):
        return False
    base = html.parent
    if path in {"", "."}:
        target = base
    else:
        target = (base / path).resolve()
    try:
        target.relative_to(SITE.resolve())
    except ValueError:
        return False
    if target.is_dir() or url.endswith("/"):
        return (target / "index.html").exists()
    if path.endswith("/"):
        return (target / "index.html").exists()
    return target.exists()


def main() -> None:
    active_nav = {
        "index.html": "Home",
        "products/index.html": "Products",
        "products/utt810/index.html": "Products",
        "downloads/index.html": "Downloads",
        "downloads/utt810/index.html": "Downloads",
        "achievements/index.html": "Achievements",
        "press/index.html": "Press",
        "team/index.html": "Team",
        "contact/index.html": "Contact",
    }
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
        ".nojekyll",
        "assets/css/styles.css",
        "assets/images/nexatom-lockup.png",
        "assets/images/nexatom-favicon-filled.png",
        "assets/images/nexatom-mark.png",
    ]
    for rel in required:
        if not (SITE / rel).exists():
            fail(f"missing site/{rel}")

    html_files = sorted(SITE.rglob("*.html"))
    for html in html_files:
        text = html.read_text(encoding="utf-8")
        if 'assets/css/styles.css' not in text:
            fail(f"{html.relative_to(ROOT)} must load assets/css/styles.css")
        if 'assets/images/nexatom-lockup.png' not in text:
            fail(f"{html.relative_to(ROOT)} must use the Nexatom header logo")
        if 'assets/images/nexatom-favicon-filled.png' not in text:
            fail(f"{html.relative_to(ROOT)} must load the Nexatom favicon mark")
        if '>nexAtom</a>' in text:
            fail(f"{html.relative_to(ROOT)} still uses text-only header branding")
        if 'href="products/' in text or 'href="downloads/' in text:
            if html.parent != SITE:
                fail(f"{html.relative_to(ROOT)} contains depth-sensitive relative nav links")
        if 'ghs.googlehosted.com' in text or 'drive.google.com' in text:
            fail(f"{html.relative_to(ROOT)} contains old Google-hosted download/media link")
        if "Nexatom Research & Instruments" in text:
            fail(f"{html.relative_to(ROOT)} has unescaped title ampersand")
        if '<header class="site-header">' not in text:
            fail(f"{html.relative_to(ROOT)} missing shared header")
        if '<footer class="site-footer">' not in text:
            fail(f"{html.relative_to(ROOT)} missing shared footer")
        if '<main class="page">' not in text:
            fail(f"{html.relative_to(ROOT)} missing page wrapper")
        if '<meta name="description"' not in text:
            fail(f"{html.relative_to(ROOT)} missing meta description")
        if "<title>" not in text:
            fail(f"{html.relative_to(ROOT)} missing title")
        rel_html = html.relative_to(SITE).as_posix()
        current_count = text.count('aria-current="page"')
        if rel_html == "404.html":
            if current_count:
                fail("site/404.html should not mark a current nav item")
        else:
            expected_current = active_nav.get(rel_html)
            if not expected_current:
                fail(f"{html.relative_to(ROOT)} missing active nav expectation")
            if current_count != 1:
                fail(f"{html.relative_to(ROOT)} must have exactly one current nav item")
            if f'aria-current="page">{expected_current}</a>' not in text:
                fail(f"{html.relative_to(ROOT)} must mark {expected_current} as current nav item")

        parser = LinkParser()
        parser.feed(text)
        for attr, value in parser.links:
            if value.startswith(("#", "mailto:", "tel:")):
                continue
            if value.startswith(("http://", "https://")):
                continue
            if value.startswith("/"):
                fail(f"{html.relative_to(ROOT)} has root-relative {attr}: {value}")
            if not internal_target_exists(html, value):
                fail(f"{html.relative_to(ROOT)} points to missing internal target: {value}")

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

    page_checks = {
        "achievements/index.html": ["precision laser system", "Raman Research Institute", "quantum and spectroscopy"],
        "press/index.html": ["DST", "Times of India", "Deccan Herald", "trademarks"],
        "team/index.html": ["highly talented and tenacious researchers", "coalition of ideas"],
        "contact/index.html": ["nexatom.research@gmail.com", "+91 8884998660", "LinkedIn"],
        "404.html": ["Page not found", "Return home"],
    }
    for rel, phrases in page_checks.items():
        text = (SITE / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"site/{rel} missing phrase: {phrase}")

    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in SITE.rglob("*") if path.is_file())
    if "Click to Downlaod" in all_text or "Click to Download Software for Nexatom UTT 810" in all_text:
        fail("old Google Sites download copy remains")
    if "https://drive.google.com" in all_text:
        fail("Google Drive URL remains in production site")
    if 'href="https://www.linkedin.com/"' in all_text:
        fail("generic LinkedIn homepage URL remains")

    required_external = [
        "https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.1/Nexatom_UTT810_Setup_1.0.1.exe",
        "https://github.com/nexatom-research/nexatom-downloads/releases/tag/time-tagger-UTT810-v1.0.1",
        "https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json",
        "https://in.linkedin.com/in/subodhvashist",
        "https://dst.gov.in/rri-spinoff-companys-tunable-lasers-could-lower-costs-quantum-optics-labs",
        "https://timesofindia.indiatimes.com/india/rris-first-spinoff-to-produce-cost-effective-laser-systems-for-quantum-optics/articleshow/111858581.cms",
        "https://www.deccanherald.com/science/rri-spin-off-companys-low-cost-laser-systems-to-boost-quantum-optics-3113282",
    ]
    for url in required_external:
        if url not in all_text:
            fail(f"missing required external URL: {url}")

    if (SITE / "CNAME").exists():
        fail("site/CNAME should not be present until the custom domain is ready for cutover")

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
