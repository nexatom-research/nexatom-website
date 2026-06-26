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
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: value or "" for name, value in attrs}
        if tag == "img":
            self.images.append(attr_map)
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
        "products/laser-systems/index.html": "Products",
        "products/time-taggers/index.html": "Products",
        "products/time-taggers/utt810/index.html": "Products",
        "products/time-taggers/utt-16in-8out/index.html": "Products",
        "products/time-taggers/utt32/index.html": "Products",
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
        "products/laser-systems/index.html",
        "products/time-taggers/index.html",
        "products/time-taggers/utt810/index.html",
        "products/time-taggers/utt-16in-8out/index.html",
        "products/time-taggers/utt32/index.html",
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
        "assets/images/laser-systems/ecdl-mount.png",
        "assets/images/laser-systems/ecdl-gui-rpi3.png",
        "assets/images/laser-systems/new-controller-sas.png",
        "assets/images/current-site/problem-solution.png",
        "assets/images/current-site/portfolio.png",
        "assets/images/current-site/closer-look.png",
        "assets/images/current-site/license-agreement-group.jpg",
        "assets/images/current-site/license-agreement-signing.jpg",
        "assets/images/current-site/press-dst.jpg",
        "assets/images/current-site/press-times-of-india.jpg",
        "assets/images/current-site/press-deccan-herald.png",
        "assets/images/current-site/team-overview.png",
        "assets/images/time-taggers/utt810-product.jpg",
        "assets/images/time-taggers/utt810-software-detail.jpg",
        "assets/images/time-taggers/utt810-box.png",
        "assets/images/time-taggers/utt810-packaging-detail.jpg",
        "assets/images/time-taggers/utt810-working-setup.jpg",
        "assets/images/time-taggers/tt-accuracy-histogram.jpg",
        "assets/images/time-taggers/tt-16-8-top.jpg",
        "assets/images/time-taggers/tt-16-8-bottom.jpg",
        "assets/images/time-taggers/tt-32-top.jpg",
        "assets/images/time-taggers/tt-32-bottom.jpg",
        "assets/videos/precision-laser-system.mp4",
        "assets/videos/precision-laser-system-poster.jpg",
        "assets/js/image-lightbox.js",
        "assets/js/video-scroll.js",
    ]
    for rel in required:
        if not (SITE / rel).exists():
            fail(f"missing site/{rel}")

    expected_expandable_images = {
        "index.html": {
            "assets/images/current-site/portfolio.png",
        },
        "products/laser-systems/index.html": {
            "../../assets/images/laser-systems/ecdl-gui-rpi3.png",
            "../../assets/images/laser-systems/new-controller-sas.png",
            "../../assets/images/laser-systems/ecdl-mount.png",
        },
        "products/time-taggers/index.html": {
            "../../assets/images/time-taggers/tt-accuracy-histogram.jpg",
        },
        "products/time-taggers/utt810/index.html": {
            "../../../assets/images/time-taggers/utt810-product.jpg",
            "../../../assets/images/time-taggers/utt810-software-detail.jpg",
            "../../../assets/images/time-taggers/utt810-box.png",
            "../../../assets/images/time-taggers/utt810-packaging-detail.jpg",
            "../../../assets/images/time-taggers/tt-accuracy-histogram.jpg",
            "../../../assets/images/time-taggers/utt810-working-setup.jpg",
        },
        "products/time-taggers/utt-16in-8out/index.html": {
            "../../../assets/images/time-taggers/tt-16-8-top.jpg",
            "../../../assets/images/time-taggers/tt-16-8-bottom.jpg",
        },
        "products/time-taggers/utt32/index.html": {
            "../../../assets/images/time-taggers/tt-32-top.jpg",
            "../../../assets/images/time-taggers/tt-32-bottom.jpg",
        },
        "achievements/index.html": {
            "../assets/images/current-site/license-agreement-group.jpg",
            "../assets/images/current-site/license-agreement-signing.jpg",
        },
        "team/index.html": {
            "../assets/images/current-site/team-overview.png",
        },
    }
    seen_expandable_images: dict[str, set[str]] = {}

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
        expandable_srcs = {
            image.get("src", "")
            for image in parser.images
            if "data-expand-image" in image
        }
        if expandable_srcs:
            seen_expandable_images[rel_html] = expandable_srcs
            allowed = expected_expandable_images.get(rel_html, set())
            unexpected = expandable_srcs - allowed
            if unexpected:
                fail(f"{html.relative_to(ROOT)} has unexpected expandable images: {sorted(unexpected)}")
            if "assets/js/image-lightbox.js" not in text:
                fail(f"{html.relative_to(ROOT)} has expandable images but does not load image-lightbox.js")
        for image in parser.images:
            if "data-expand-image" in image and "brand-logo" in image.get("class", ""):
                fail(f"{html.relative_to(ROOT)} makes the header logo expandable")
            if "data-expand-image" in image and any(
                forbidden in image.get("src", "")
                for forbidden in [
                    "nexatom-lockup.png",
                    "nexatom-mark.png",
                    "nexatom-favicon",
                    "press-dst.jpg",
                    "press-times-of-india.jpg",
                    "press-deccan-herald.png",
                ]
            ):
                fail(f"{html.relative_to(ROOT)} makes a logo/press asset expandable: {image.get('src', '')}")
        for attr, value in parser.links:
            if value.startswith(("#", "mailto:", "tel:")):
                continue
            if value.startswith(("http://", "https://")):
                continue
            if value.startswith("/"):
                fail(f"{html.relative_to(ROOT)} has root-relative {attr}: {value}")
            if not internal_target_exists(html, value):
                fail(f"{html.relative_to(ROOT)} points to missing internal target: {value}")

    for rel_html, expected in expected_expandable_images.items():
        seen = seen_expandable_images.get(rel_html, set())
        if seen != expected:
            fail(f"site/{rel_html} expandable image set mismatch: expected {sorted(expected)}, saw {sorted(seen)}")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    for phrase in [
        "Precision laser systems, time taggers, and scientific instruments",
        "Let's build together",
        "Explore Products",
        "Discuss an Instrument",
        "Product areas",
        "Precision laser systems",
        "View laser systems",
        "Universal time taggers",
        "View time taggers",
        "Custom scientific instrumentation",
        "Start a discussion",
        "assets/images/time-taggers/utt810-working-setup.jpg",
        "From research capability to practical instruments",
        "View Products",
        "Meet the Team",
        "assets/images/current-site/portfolio.png",
        "Research-led instrumentation work",
        "Raman Research Institute license agreement",
        "assets/images/current-site/license-agreement-group.jpg",
        "View Achievements",
        "View Press",
        "Discuss an instrument or product requirement",
        "Contact Nexatom",
        "Download UTT810 Software",
        "subodh@nexatom.in",
    ]:
        if phrase not in home:
            fail(f"homepage missing phrase: {phrase}")

    products = (SITE / "products/index.html").read_text(encoding="utf-8")
    for phrase in [
        "Nexatom products",
        "Precision laser systems",
        "Laser control interface showing input and error signal plots",
        "View laser systems",
        "Universal time taggers",
        "Closer look at Nexatom instrumentation and laboratory work",
        "Nexatom Universal Time Taggers",
        "16-in / 8-out custom board",
        "32-channel time tagger board",
        "View time taggers",
    ]:
        if phrase not in products:
            fail(f"products index missing phrase: {phrase}")

    lasers = (SITE / "products/laser-systems/index.html").read_text(encoding="utf-8")
    for phrase in [
        "Precision laser systems",
        "Hardware, control interfaces, and laboratory operation",
        "External-cavity diode laser hardware",
        "Laser control interfaces for laboratory operation, spectroscopy, and stabilization signals",
        "data-scroll-video",
        "assets/videos/precision-laser-system.mp4",
        "assets/videos/precision-laser-system-poster.jpg",
        "assets/js/video-scroll.js",
        "Quantum optics",
        "Spectroscopy",
        "Custom integration",
    ]:
        if phrase not in lasers:
            fail(f"laser systems page missing phrase: {phrase}")

    family = (SITE / "products/time-taggers/index.html").read_text(encoding="utf-8")
    for phrase in [
        "Nexatom Universal Time Taggers",
        "Time-tagging hardware platforms",
        "UTT810 is the 8-channel model",
        "16-in / 8-out custom board",
        "32-channel time tagger board",
        "24.5 ps FWHM / 10.5 ps RMS",
    ]:
        if phrase not in family:
            fail(f"time tagger family page missing phrase: {phrase}")

    product = (SITE / "products/time-taggers/utt810/index.html").read_text(encoding="utf-8")
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
        "FCS, DLS, and DCS",
        "Biology and biophysics",
        "Multi-channel event timing",
        "combined coincidence peak of approximately 49 ps FWHM / 20.81 ps RMS",
        "24.5 ps FWHM / 10.5 ps RMS",
        "Measured performance",
    ]:
        if phrase not in product:
            fail(f"product page missing phrase: {phrase}")

    board_16 = (SITE / "products/time-taggers/utt-16in-8out/index.html").read_text(encoding="utf-8")
    for phrase in [
        "16-in / 8-out custom time tagger board",
        "Hardware overview",
        "Configuration",
        "Custom board for 16-input, 8-output timing systems",
    ]:
        if phrase not in board_16:
            fail(f"16-in / 8-out board page missing phrase: {phrase}")

    board_32 = (SITE / "products/time-taggers/utt32/index.html").read_text(encoding="utf-8")
    for phrase in [
        "32-channel time tagger board",
        "32-channel, 10 ps class",
        "Hardware overview",
        "Configuration",
        "Custom board for high-channel-count timing systems",
    ]:
        if phrase not in board_32:
            fail(f"32-channel board page missing phrase: {phrase}")

    download = (SITE / "downloads/utt810/index.html").read_text(encoding="utf-8")
    for phrase in [
        "Nexatom UTT810 Time Tagger Software",
        "Download for Windows",
        "1.0.2",
        "89.11 MB",
        "fa00a4b2a2814b0479027e3659a19cba28214cd1e4768956890c2958d06e02e5",
        "After first install, future updates are available inside the app.",
        "https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.2/Nexatom_UTT810_Setup_1.0.2.exe",
        "https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json",
    ]:
        if phrase not in download:
            fail(f"download page missing phrase: {phrase}")

    page_checks = {
        "achievements/index.html": ["Research-led instrumentation milestones", "Raman Research Institute", "quantum and spectroscopy", "License agreement signing"],
        "press/index.html": ["DST", "Times of India", "Deccan Herald", "press-dst.jpg", "press-times-of-india.jpg", "press-deccan-herald.png", "Trademarks"],
        "team/index.html": ["highly talented and tenacious researchers", "researchers and engineers", "team-overview.png"],
        "contact/index.html": ["subodh@nexatom.in", "+91 8884998660", "LinkedIn", "nexatom-lockup.png"],
        "404.html": ["Page not found", "Return home"],
    }
    for rel, phrases in page_checks.items():
        text = (SITE / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"site/{rel} missing phrase: {phrase}")

    achievements = (SITE / "achievements/index.html").read_text(encoding="utf-8")
    for phrase in [
        "External-cavity diode laser hardware",
        "data-scroll-video",
        "precision-laser-system.mp4",
    ]:
        if phrase in achievements:
            fail(f"achievements page should not repeat laser product media: {phrase}")

    all_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in SITE.rglob("*") if path.is_file())
    if "Click to Downlaod" in all_text or "Click to Download Software for Nexatom UTT 810" in all_text:
        fail("old Google Sites download copy remains")
    if "https://drive.google.com" in all_text:
        fail("Google Drive URL remains in production site")
    if "teaser_nexatom_hq.mkv" in all_text:
        fail("source MKV should not be referenced by production site")
    if 'href="https://www.linkedin.com/"' in all_text:
        fail("generic LinkedIn homepage URL remains")
    for phrase in [
        "specified timing jitter",
        "timing jitter specification",
        "Relevant workflows",
        "Product packaging and identity view",
        "Release details",
        "Updater manifest",
        "latest.json technical metadata",
        "The product directory for",
        "public Windows",
        "Hardware class",
        "hardware configuration",
        "coalition of ideas",
        "practical, tangible, and real changes",
        "public references",
        "informational and press coverage context",
        "release contexts",
    ]:
        if phrase in all_text:
            fail(f"internal or awkward public copy remains: {phrase}")

    required_external = [
        "https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.2/Nexatom_UTT810_Setup_1.0.2.exe",
        "https://github.com/nexatom-research/nexatom-downloads/releases/tag/time-tagger-UTT810-v1.0.2",
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
