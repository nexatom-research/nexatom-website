# Nexatom Website First Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first static Nexatom Research & Instruments website with a company-first homepage and strong UTT810 product/download path.

**Architecture:** The production site lives under `site/` to keep planning docs, mockups, and source PDFs out of the GitHub Pages publish root. The site is plain static HTML/CSS with shared global styling, repeated navigation/footer markup, root-relative URLs, and no runtime JavaScript requirement. GitHub Pages deployment uses an Actions workflow that uploads only `site/`.

**Tech Stack:** Static HTML5, CSS3, GitHub Pages Actions deployment, PowerShell/Python standard-library verification commands.

**Deployment Decision:** This plan intentionally uses GitHub Pages source `GitHub Actions`, not `Deploy from branch`. Root-relative URLs are designed for `http://localhost:8000/` during local verification and `https://www.nexatom.in/` after custom-domain launch; they are not intended to support repository-path previews such as `https://nexatom-research.github.io/nexatom-website/`.

---

## File Structure

Production files to create:

```text
site/
  index.html
  products/
    index.html
    utt810/
      index.html
  downloads/
    index.html
    utt810/
      index.html
  achievements/
    index.html
  press/
    index.html
  team/
    index.html
  contact/
    index.html
  assets/
    css/
      styles.css
  CNAME
  .nojekyll
  404.html
  robots.txt
  sitemap.xml
.github/
  workflows/
    pages.yml
tools/
  verify_site.py
```

Files intentionally not published:

- `docs/`
- `mockups/`
- `.superpowers/`
- `time_tagger_precision_detail_specification.pdf`
- `Nexatom_TT_Specifications (1).pdf`

Shared implementation rules:

- Internal links use root-relative URLs such as `/products/utt810/`.
- Production CSS is loaded from `/assets/css/styles.css`.
- The download page uses pinned release metadata from the live manifest at implementation time.
- No production page links to the old Google Drive installer.
- No production page depends on `.superpowers/` or `mockups/`.
- Primary nav labels `Products` and `Downloads` link directly to `/products/utt810/` and `/downloads/utt810/` for the first pass. The `/products/` and `/downloads/` index pages still exist for direct visitors and search engines.
- Favicon and brand icons are deliberately deferred until owned logo/source assets are available.

---

### Task 1: Add Publish Boundary And Deployment Skeleton

**Files:**
- Create: `site/CNAME`
- Create: `site/.nojekyll`
- Create: `site/robots.txt`
- Create: `site/sitemap.xml`
- Create: `.github/workflows/pages.yml`
- Create: `tools/verify_site.py`
- Modify: `.gitignore`

- [ ] **Step 1: Add temporary failing verification script**

Create `tools/verify_site.py` with this exact content:

```python
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
```

- [ ] **Step 2: Run verification and confirm it fails**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: missing site/index.html
```

- [ ] **Step 3: Create deployment skeleton files**

Create `site/CNAME`:

```text
www.nexatom.in
```

Create empty `site/.nojekyll`.

Create `site/robots.txt`:

```text
User-agent: *
Allow: /

Sitemap: https://www.nexatom.in/sitemap.xml
```

Create `site/sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://www.nexatom.in/</loc></url>
  <url><loc>https://www.nexatom.in/products/</loc></url>
  <url><loc>https://www.nexatom.in/products/utt810/</loc></url>
  <url><loc>https://www.nexatom.in/downloads/</loc></url>
  <url><loc>https://www.nexatom.in/downloads/utt810/</loc></url>
  <url><loc>https://www.nexatom.in/achievements/</loc></url>
  <url><loc>https://www.nexatom.in/press/</loc></url>
  <url><loc>https://www.nexatom.in/team/</loc></url>
  <url><loc>https://www.nexatom.in/contact/</loc></url>
</urlset>
```

Create `.github/workflows/pages.yml`:

```yaml
name: Deploy static site to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

In GitHub repository settings, Pages source must be set to `GitHub Actions`. Do not configure Pages as `Deploy from branch`, because that can expose `docs/`, `mockups/`, and local PDFs.

Create `.gitignore` if missing, or append these lines:

```gitignore
.superpowers/
```

- [ ] **Step 4: Add minimal scaffold pages so skeleton verification passes**

Create each required HTML file with this minimal scaffold, changing only the `<title>` and `<h1>` text:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nexatom Research & Instruments</title>
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
  <main>
    <h1>Nexatom Research & Instruments</h1>
  </main>
</body>
</html>
```

Create `site/assets/css/styles.css`:

```css
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: #162026;
  background: #fff;
}
```

- [ ] **Step 5: Run verification and confirm it passes**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 6: Commit skeleton**

Run:

```powershell
git add .github/workflows/pages.yml .gitignore site tools/verify_site.py
git commit -m "Add static site deployment skeleton"
```

---

### Task 2: Build Shared CSS, Header, Footer, And Technical Visual System

**Files:**
- Modify: `site/assets/css/styles.css`
- Modify: all `site/**/*.html`

- [ ] **Step 1: Expand verifier for shared layout requirements**

Modify `tools/verify_site.py` by adding these checks inside `main()` after the required-file loop:

```python
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
```

- [ ] **Step 2: Run verification and confirm it fails**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: site/index.html missing shared header
```

- [ ] **Step 3: Replace `site/assets/css/styles.css`**

Use this CSS as the shared visual system:

```css
:root {
  --ink: #162026;
  --muted: #5b6870;
  --line: #d8e1e6;
  --soft: #f4f7f8;
  --panel: #17252d;
  --panel-2: #22343d;
  --cyan: #0b6f82;
  --red: #b84034;
  --gold: #b88428;
  --green: #2d7d56;
  --white: #fff;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: var(--ink);
  background: var(--white);
  line-height: 1.55;
}

a { color: var(--cyan); }

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 18px 32px;
  background: rgba(255, 255, 255, 0.96);
  border-bottom: 1px solid var(--line);
}

.brand {
  color: var(--ink);
  font-weight: 700;
  text-decoration: none;
}

.site-nav {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
  font-size: 14px;
}

.site-nav a {
  color: var(--muted);
  text-decoration: none;
}

.site-nav a:hover { color: var(--cyan); }

.page {
  max-width: 1160px;
  margin: 0 auto;
  padding: 40px 24px 72px;
}

.section {
  padding: 52px 0;
  border-bottom: 1px solid var(--line);
}

.section:last-child { border-bottom: 0; }

.hero {
  min-height: 480px;
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(320px, 0.92fr);
  gap: 48px;
  align-items: center;
}

.hero.compact { min-height: 320px; }

.eyebrow {
  margin-bottom: 10px;
  color: var(--cyan);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

h1, h2, h3 {
  margin: 0 0 14px;
  line-height: 1.14;
  letter-spacing: 0;
}

h1 { max-width: 820px; font-size: 44px; }
h2 { font-size: 30px; }
h3 { font-size: 19px; }

p {
  max-width: 780px;
  margin: 0 0 16px;
  color: var(--muted);
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 18px;
  border: 1px solid var(--cyan);
  border-radius: 4px;
  background: var(--cyan);
  color: var(--white);
  font-weight: 700;
  text-decoration: none;
}

.button.secondary {
  background: var(--white);
  color: var(--cyan);
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 22px;
}

.grid.four {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.card, .metric, .download-panel {
  border: 1px solid var(--line);
  border-radius: 7px;
  background: var(--soft);
  padding: 22px;
}

.metric strong {
  display: block;
  margin-bottom: 4px;
  color: var(--ink);
  font-size: 26px;
}

.instrument {
  border: 1px solid #31464f;
  border-radius: 8px;
  padding: 22px;
  color: #d9e8ed;
  background: linear-gradient(145deg, var(--panel), var(--panel-2));
  box-shadow: 0 22px 42px rgba(20, 33, 41, 0.18);
}

.instrument-top {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid #3b515b;
}

.screen {
  position: relative;
  min-height: 145px;
  margin: 18px 0;
  overflow: hidden;
  border: 1px solid #415861;
  border-radius: 5px;
  background: #0d171c;
}

.trace {
  position: absolute;
  left: 14px;
  right: 14px;
  height: 2px;
  background: #3c5d66;
}

.trace.one { top: 34px; }
.trace.two { top: 72px; }
.trace.three { top: 110px; }

.pulse {
  position: absolute;
  top: -13px;
  width: 5px;
  height: 28px;
  background: #51c7d9;
  box-shadow: 0 0 12px rgba(81, 199, 217, 0.45);
}

.pulse.gold { background: #e0aa45; }
.pulse.red { background: #df6a5f; }

.ports {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 9px;
}

.port {
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  border: 3px solid #536972;
  border-radius: 50%;
  background: #0f171b;
  color: #9cb0b8;
  font-size: 11px;
}

.mini-plot {
  position: relative;
  min-height: 150px;
  margin-bottom: 12px;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 5px;
  background:
    linear-gradient(90deg, transparent 19px, rgba(11, 111, 130, 0.08) 20px),
    linear-gradient(transparent 19px, rgba(11, 111, 130, 0.08) 20px),
    #fff;
  background-size: 20px 20px;
}

.peak {
  position: absolute;
  bottom: 22px;
  left: 50%;
  width: 96px;
  height: 96px;
  transform: translateX(-50%);
  background: linear-gradient(180deg, rgba(184, 64, 52, 0.85), rgba(184, 64, 52, 0.05));
  clip-path: polygon(0 100%, 12% 86%, 22% 70%, 34% 48%, 46% 18%, 54% 12%, 66% 44%, 78% 70%, 90% 88%, 100% 100%);
}

.pipeline {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  align-items: center;
  min-height: 150px;
  padding: 18px;
}

.node {
  border: 1px solid var(--line);
  border-radius: 5px;
  background: #fff;
  padding: 12px;
  text-align: center;
  font-size: 13px;
  font-weight: 700;
}

.spec-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 14px;
}

.spec-table th,
.spec-table td {
  padding: 11px 8px;
  border-bottom: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

.spec-table th {
  width: 34%;
  color: var(--muted);
}

code {
  word-break: break-all;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: #fff;
  padding: 3px 6px;
}

.site-footer {
  border-top: 1px solid var(--line);
  padding: 28px 32px;
  color: var(--muted);
  font-size: 14px;
}

.site-footer-inner {
  max-width: 1160px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

@media (max-width: 860px) {
  .site-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .hero {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  h1 { font-size: 34px; }
  h2 { font-size: 25px; }

  .grid,
  .grid.four {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 4: Add shared header/footer markup to every page**

Every page should use this header immediately after `<body>`:

```html
<header class="site-header">
  <a class="brand" href="/">nexAtom</a>
  <nav class="site-nav" aria-label="Primary navigation">
    <a href="/">Home</a>
    <a href="/products/utt810/">Products</a>
    <a href="/downloads/utt810/">Downloads</a>
    <a href="/achievements/">Achievements</a>
    <a href="/press/">Press</a>
    <a href="/team/">Team</a>
    <a href="/contact/">Contact</a>
  </nav>
</header>
```

Every page should use this footer before `</body>`:

```html
<footer class="site-footer">
  <div class="site-footer-inner">
    <span>Nexatom Research &amp; Instruments Pvt. Ltd.</span>
    <span><a href="mailto:nexatom.research@gmail.com">nexatom.research@gmail.com</a> | +91 8884998660</span>
  </div>
</footer>
```

- [ ] **Step 5: Run verification**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 6: Commit shared layout**

Run:

```powershell
git add site tools/verify_site.py
git commit -m "Add shared static site layout"
```

---

### Task 3: Implement Homepage And Index Pages

**Files:**
- Modify: `site/index.html`
- Modify: `site/products/index.html`
- Modify: `site/downloads/index.html`
- Modify: `tools/verify_site.py`

- [ ] **Step 1: Add homepage content checks**

Add this to `tools/verify_site.py` inside `main()` after shared layout checks:

```python
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
        "Press coverage",
        "Subodh Vashist",
        "nexatom.research@gmail.com",
    ]:
        if phrase not in home:
            fail(f"homepage missing phrase: {phrase}")
```

- [ ] **Step 2: Run verification and confirm it fails**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: homepage missing phrase: Indigenous precision laser sources and scientific instruments
```

- [ ] **Step 3: Replace `site/index.html`**

Replace only the existing `<main>...</main>` block in `site/index.html` with this content. Preserve the existing `<head>`, stylesheet link, shared header, and shared footer:

```html
<main class="page">
  <section class="hero">
    <div>
      <div class="eyebrow">Nexatom Research &amp; Instruments</div>
      <h1>Indigenous precision laser sources and scientific instruments</h1>
      <p><strong>Let's build together.</strong></p>
      <p>nexAtom mobilizes research knowledge into practical high-technology instruments for research and industry.</p>
      <div class="actions">
        <a class="button" href="/products/utt810/">Explore UTT810</a>
        <a class="button secondary" href="/downloads/utt810/">Download Software</a>
      </div>
    </div>
    <div class="instrument" aria-label="UTT810 technical timing visual">
      <div class="instrument-top"><strong>NEXATOM UTT810</strong><span>Universal Time Tagger</span></div>
      <div class="screen">
        <div class="trace one"><span class="pulse" style="left:12%"></span><span class="pulse" style="left:47%"></span><span class="pulse" style="left:81%"></span></div>
        <div class="trace two"><span class="pulse gold" style="left:24%"></span><span class="pulse gold" style="left:53%"></span></div>
        <div class="trace three"><span class="pulse red" style="left:36%"></span><span class="pulse red" style="left:72%"></span></div>
      </div>
      <div class="ports">
        <span class="port">1</span><span class="port">2</span><span class="port">3</span><span class="port">4</span>
        <span class="port">5</span><span class="port">6</span><span class="port">7</span><span class="port">8</span>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="eyebrow">Featured product</div>
    <h2>Nexatom UTT810 Universal Time Tagger</h2>
    <p>An 8-channel USB time tagger for coincidence, histogram, correlation, and synchronized event-timing measurements.</p>
    <div class="grid four">
      <div class="metric"><strong>8</strong>input channels</div>
      <div class="metric"><strong>1 ps</strong>time bin width</div>
      <div class="metric"><strong>&lt;10 ps</strong>timing jitter specification</div>
      <div class="metric"><strong>USB 3</strong>&gt;300 MB/s data transfer</div>
    </div>
  </section>

  <section class="section">
    <h2>About Us</h2>
    <p>Nexatom Research &amp; Instruments develops indigenous high-technology solutions for precision lasers, laser-based instruments, and scientific measurement systems.</p>
  </section>

  <section class="section">
    <h2>Problem and Solution</h2>
    <p>Research and industry users often depend on expensive imported laser and measurement systems with long delivery times and limited customization. Nexatom works to convert local R&amp;D capability into practical, customizable instruments.</p>
  </section>

  <section class="section">
    <h2>Our Portfolio</h2>
    <p>Current work spans precision laser systems, tunable laser solutions, custom scientific instrumentation, and the UTT810 Universal Time Tagger.</p>
  </section>

  <section class="section">
    <h2>A Closer Look</h2>
    <p>Explore Nexatom's precision instrumentation work, public achievements, and release-backed UTT810 software downloads.</p>
  </section>

  <section class="section">
    <h2>Achievements and press coverage</h2>
    <p>Read about Nexatom's precision laser work, RRI license agreement milestone, and public references in DST, Times of India, and Deccan Herald coverage.</p>
    <div class="actions">
      <a class="button secondary" href="/achievements/">View Achievements</a>
      <a class="button secondary" href="/press/">View Press</a>
    </div>
  </section>

  <section class="section">
    <h2>Contact Us</h2>
    <p><a href="mailto:nexatom.research@gmail.com">nexatom.research@gmail.com</a> | +91 8884998660</p>
    <p>LinkedIn: <a href="https://in.linkedin.com/in/subodhvashist">Subodh Vashist</a></p>
  </section>
</main>
```

- [ ] **Step 4: Replace the `<main>` block in `site/products/index.html`**

Main content:

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Products</div>
      <h1>Nexatom products</h1>
      <p>The current public product path focuses on the Nexatom UTT810 Universal Time Tagger.</p>
      <div class="actions">
        <a class="button" href="/products/utt810/">Explore UTT810</a>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 5: Replace the `<main>` block in `site/downloads/index.html`**

Main content:

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Downloads</div>
      <h1>Software downloads</h1>
      <p>Download the Windows installer for the Nexatom UTT810 Time Tagger software.</p>
      <div class="actions">
        <a class="button" href="/downloads/utt810/">Download UTT810 software</a>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 6: Run verification**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 7: Commit homepage and indexes**

Run:

```powershell
git add site tools/verify_site.py
git commit -m "Build homepage and index pages"
```

---

### Task 4: Implement UTT810 Product Page

**Files:**
- Modify: `site/products/utt810/index.html`
- Modify: `tools/verify_site.py`

- [ ] **Step 1: Add product page checks**

Add this to `tools/verify_site.py`:

```python
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
```

- [ ] **Step 2: Run verification and confirm it fails**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: product page missing phrase: Nexatom UTT810 Universal Time Tagger
```

- [ ] **Step 3: Replace the `<main>` block in `site/products/utt810/index.html`**

Main content:

```html
<main class="page">
  <section class="hero">
    <div>
      <div class="eyebrow">Product / UTT810</div>
      <h1>Nexatom UTT810 Universal Time Tagger</h1>
      <p>An 8-channel USB time tagger for coincidence, histogram, correlation, and synchronized event-timing measurements.</p>
      <div class="actions">
        <a class="button" href="/downloads/utt810/">Download Software</a>
        <a class="button secondary" href="/contact/">Contact Nexatom</a>
      </div>
    </div>
    <div class="instrument" aria-label="UTT810 front-panel timing visual">
      <div class="instrument-top"><strong>UTT810</strong><span>8-channel timing</span></div>
      <div class="screen">
        <div class="trace one"><span class="pulse" style="left:16%"></span><span class="pulse" style="left:58%"></span></div>
        <div class="trace two"><span class="pulse gold" style="left:25%"></span><span class="pulse gold" style="left:66%"></span></div>
        <div class="trace three"><span class="pulse red" style="left:42%"></span><span class="pulse red" style="left:78%"></span></div>
      </div>
      <div class="ports">
        <span class="port">1</span><span class="port">2</span><span class="port">3</span><span class="port">4</span>
        <span class="port">5</span><span class="port">6</span><span class="port">7</span><span class="port">8</span>
      </div>
    </div>
  </section>

  <section class="section">
    <h2>Specification highlights</h2>
    <div class="grid four">
      <div class="metric"><strong>8</strong>input channels</div>
      <div class="metric"><strong>1 ps</strong>time bin width</div>
      <div class="metric"><strong>&lt;10 ps</strong>timing jitter specification</div>
      <div class="metric"><strong>USB 3</strong>USB 3 data transfer above 300 MB/s</div>
    </div>
    <div class="grid">
      <div class="metric"><strong>4 ns</strong>dead time</div>
      <div class="metric"><strong>0-2.5 V</strong>threshold in 1 mV steps</div>
      <div class="metric"><strong>10 MHz</strong>external TTL sync support</div>
    </div>
  </section>

  <section class="section">
    <h2>Relevant workflows</h2>
    <div class="grid">
      <div class="card"><h3>Coincidence counting</h3><p>Multi-fold coincidence histograms up to 8 channels.</p></div>
      <div class="card"><h3>Correlation measurements</h3><p>Real-time linear and multi-tau auto/cross correlation modes with minimum 8 ns bin width.</p></div>
      <div class="card"><h3>Synchronized timing</h3><p>External 10 MHz TTL clock support through GPIO pin 2.</p></div>
      <div class="card"><h3>Quantum optics</h3><p>Relevant for timing workflows used in quantum optics experiments.</p></div>
      <div class="card"><h3>Spectroscopy</h3><p>Relevant for time-correlated measurements and spectroscopy workflows.</p></div>
      <div class="card"><h3>Multi-channel event timing</h3><p>Eight input channels support multi-channel event timing and analysis.</p></div>
    </div>
  </section>

  <section class="section">
    <h2>Real-time FPGA processing</h2>
    <div class="grid">
      <div class="card">
        <div class="mini-plot"><div class="peak"></div></div>
        <h3>Coincidence peak</h3>
        <p>Visualizes time-correlated event measurements and validation-style analysis.</p>
      </div>
      <div class="card">
        <div class="mini-plot"><div class="pipeline"><span class="node">Inputs</span><span class="node">FPGA</span><span class="node">GUI/API</span></div></div>
        <h3>Histogram pipeline</h3>
        <p>Real-time FPGA time histogram with minimum 1 ps bin width and multi-stop support.</p>
      </div>
      <div class="card">
        <div class="mini-plot"><div class="pipeline"><span class="node">10 MHz TTL</span><span class="node">GPIO 2</span><span class="node">Sync</span></div></div>
        <h3>External sync</h3>
        <p>External 10 MHz TTL synchronization support for coordinated instrument timing.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <h2>Grouped specifications</h2>
    <table class="spec-table">
      <tr><th>Model</th><td>Nexatom Universal Time Tagger, UTT_810 / UTT810</td></tr>
      <tr><th>Channels</th><td>8 input channels</td></tr>
      <tr><th>Timing</th><td>1 ps time bin width, &lt;10 ps timing jitter specification, 4 ns dead time</td></tr>
      <tr><th>Processing</th><td>Time histogram, coincidence histogram, and correlation measurement with Real-time FPGA processing</td></tr>
      <tr><th>Inputs</th><td>0 to 5 V input range, 0 to 2.5 V threshold in 1 mV steps, 1 mV to 100 mV hysteresis, 50 ohms impedance, 1 ps to 4 ns physical delay</td></tr>
      <tr><th>Interface</th><td>USB 3 data transfer above 300 MB/s</td></tr>
      <tr><th>Software</th><td>GUI and API with absolute time-tag saving</td></tr>
      <tr><th>Synchronization</th><td>External 10 MHz TTL clock signal on GPIO pin 2. The GUI detects a valid clock when Use External Sync is enabled.</td></tr>
    </table>
  </section>

  <section class="section">
    <h2>Validation note</h2>
    <p>Internal two-channel validation showed an effective single-channel contribution of 24.5 ps FWHM / 10.5 ps RMS in the test setup, including signal source and measurement-chain uncertainty.</p>
  </section>

  <section class="section">
    <h2>Next steps</h2>
    <div class="actions">
      <a class="button" href="/downloads/utt810/">Download Windows software</a>
      <a class="button secondary" href="/contact/">Contact Nexatom</a>
    </div>
  </section>
</main>
```

- [ ] **Step 4: Run verification**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 5: Commit product page**

Run:

```powershell
git add site/products/utt810/index.html tools/verify_site.py
git commit -m "Build UTT810 product page"
```

---

### Task 5: Implement UTT810 Download Page

**Files:**
- Modify: `site/downloads/utt810/index.html`
- Modify: `tools/verify_site.py`

- [ ] **Step 1: Add download metadata checks**

Add this to `tools/verify_site.py`:

```python
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
```

- [ ] **Step 2: Run verification and confirm it fails**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: download page missing phrase: Nexatom UTT810 Time Tagger Software
```

- [ ] **Step 3: Replace the `<main>` block in `site/downloads/utt810/index.html`**

Main content:

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Downloads / UTT810</div>
      <h1>Nexatom UTT810 Time Tagger Software</h1>
      <p>Windows installer for first-time setup of the Nexatom UTT810 Time Tagger software.</p>
      <div class="actions">
        <a class="button" href="https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.1/Nexatom_UTT810_Setup_1.0.1.exe">Download for Windows</a>
        <a class="button secondary" href="https://github.com/nexatom-research/nexatom-downloads/releases/tag/time-tagger-UTT810-v1.0.1">View GitHub Release</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="download-panel">
      <h2>Release details</h2>
      <table class="spec-table">
        <tr><th>Version</th><td>1.0.1</td></tr>
        <tr><th>File</th><td>Nexatom_UTT810_Setup_1.0.1.exe</td></tr>
        <tr><th>File size</th><td>85,780,093 bytes / 85.78 MB</td></tr>
        <tr><th>SHA256</th><td><code>cee5a78865e0b0923649c4f922327ab54de059721135fefa8bda499ed6510e3a</code></td></tr>
        <tr><th>Updater manifest</th><td><a href="https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json">latest.json technical metadata</a></td></tr>
      </table>
      <p>After first install, future updates are available inside the app.</p>
    </div>
  </section>

  <section class="section">
    <h2>Installation support</h2>
    <p>For installation issues, contact <a href="mailto:nexatom.research@gmail.com">nexatom.research@gmail.com</a> or call +91 8884998660.</p>
  </section>
</main>
```

- [ ] **Step 4: Run verification**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 5: Commit download page**

Run:

```powershell
git add site/downloads/utt810/index.html tools/verify_site.py
git commit -m "Build UTT810 download page"
```

---

### Task 6: Implement Achievements, Press, Team, Contact, And 404

**Files:**
- Modify: `site/achievements/index.html`
- Modify: `site/press/index.html`
- Modify: `site/team/index.html`
- Modify: `site/contact/index.html`
- Modify: `site/404.html`
- Modify: `tools/verify_site.py`

- [ ] **Step 1: Add secondary page checks**

Add this to `tools/verify_site.py`:

```python
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
```

- [ ] **Step 2: Run verification and confirm it fails**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: site/achievements/index.html missing phrase: precision laser system
```

- [ ] **Step 3: Replace the `<main>` block in `site/achievements/index.html`**

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Achievements</div>
      <h1>Research-led instrumentation milestones</h1>
      <p>A glimpse at Nexatom's precision laser system and translation of research capability into practical instruments.</p>
    </div>
  </section>
  <section class="section">
    <h2>Precision laser system</h2>
    <p>Ultra-stable, high-precision, dual-channel tunable lasers of various powers, form factors, and custom integration configurations are part of Nexatom's instrumentation work.</p>
  </section>
  <section class="section">
    <h2>RRI license agreement milestone</h2>
    <p>Raman Research Institute, Bangalore and Nexatom Research and Instruments Pvt. Ltd. entered an agreement to build highly integrated, ultra-precision, continuously tunable CW lasers for quantum and spectroscopy applications.</p>
  </section>
</main>
```

- [ ] **Step 4: Replace the `<main>` block in `site/press/index.html`**

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Press</div>
      <h1>Press coverage</h1>
      <p>Selected public references to Nexatom's work and recognition.</p>
    </div>
  </section>
  <section class="section">
    <div class="grid">
      <div class="card"><h2>DST</h2><p>DST recognition of nexAtom's potential in indigenous high-technology development.</p></div>
      <div class="card"><h2>Times of India</h2><p>Coverage referencing Nexatom's role in National Quantum Mission related precision tunable CW lasers.</p></div>
      <div class="card"><h2>Deccan Herald</h2><p>Coverage on the indigenous quantum-enabling ecosystem and RRI/Nexatom's role.</p></div>
    </div>
  </section>
  <section class="section">
    <p>All trademarks, logos, brand names, article titles, and publication references belong to their respective owners. References are provided for informational and press coverage context.</p>
  </section>
</main>
```

- [ ] **Step 5: Replace the `<main>` block in `site/team/index.html`**

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Team</div>
      <h1>Nexatom team</h1>
      <p>A team of highly talented and tenacious researchers with extensive knowledge in their respective domains of expertise.</p>
    </div>
  </section>
  <section class="section">
    <h2>A coalition of ideas</h2>
    <p>nexAtom is a coalition of ideas by experts who want to see practical, tangible, and real changes in high-tech lasers, laser-based instruments, and technology translation to applications.</p>
  </section>
</main>
```

- [ ] **Step 6: Replace the `<main>` block in `site/contact/index.html`**

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">Contact</div>
      <h1>Contact Nexatom</h1>
      <p>Reach out to us via mail or call us for product, collaboration, and installation support.</p>
      <div class="actions">
        <a class="button" href="mailto:nexatom.research@gmail.com">Email Nexatom</a>
        <a class="button secondary" href="tel:+918884998660">Call +91 8884998660</a>
      </div>
    </div>
  </section>
  <section class="section">
    <h2>Contact details</h2>
    <p>Email: <a href="mailto:nexatom.research@gmail.com">nexatom.research@gmail.com</a></p>
    <p>Phone: +91 8884998660</p>
    <p>LinkedIn: <a href="https://in.linkedin.com/in/subodhvashist">Subodh Vashist</a></p>
  </section>
</main>
```

- [ ] **Step 7: Replace the `<main>` block in `site/404.html`**

```html
<main class="page">
  <section class="hero compact">
    <div>
      <div class="eyebrow">404</div>
      <h1>Page not found</h1>
      <p>The page you are looking for is not available on the Nexatom website.</p>
      <div class="actions">
        <a class="button" href="/">Return home</a>
      </div>
    </div>
  </section>
</main>
```

- [ ] **Step 8: Run verification**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 9: Commit secondary pages**

Run:

```powershell
git add site tools/verify_site.py
git commit -m "Build company information pages"
```

---

### Task 7: Final Metadata, Local Server Verification, And Launch Readiness

**Files:**
- Modify: all `site/**/*.html`
- Modify: `site/sitemap.xml`
- Modify: `tools/verify_site.py`

- [ ] **Step 1: Add final metadata checks**

Add these imports near the top of `tools/verify_site.py`:

```python
from html.parser import HTMLParser
from urllib.parse import urlparse
```

Add this parser class below `fail()`:

```python
class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.links.append((name, value))


def internal_target_exists(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path
    if not path.startswith("/"):
        return False
    if path == "/":
        return (SITE / "index.html").exists()
    if path.endswith("/"):
        return (SITE / path.lstrip("/") / "index.html").exists()
    return (SITE / path.lstrip("/")).exists()
```

Add these checks to `main()`:

```python
    for html in sorted(SITE.rglob("*.html")):
        text = html.read_text(encoding="utf-8")
        if '<meta name="description"' not in text:
            fail(f"{html.relative_to(ROOT)} missing meta description")
        if "<title>" not in text:
            fail(f"{html.relative_to(ROOT)} missing title")

        parser = LinkParser()
        parser.feed(text)
        for attr, value in parser.links:
            if value.startswith(("#", "mailto:", "tel:")):
                continue
            if value.startswith(("http://", "https://")):
                continue
            if not value.startswith("/"):
                fail(f"{html.relative_to(ROOT)} has non-root-relative {attr}: {value}")
            if not internal_target_exists(value):
                fail(f"{html.relative_to(ROOT)} points to missing internal target: {value}")

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
    ]
    for url in required_external:
        if url not in all_text:
            fail(f"missing required external URL: {url}")
```

- [ ] **Step 2: Run verification and confirm it fails on missing descriptions**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
FAIL: site/index.html missing meta description
```

- [ ] **Step 3: Add unique meta descriptions**

Each page should include a description in `<head>`, for example:

```html
<meta name="description" content="Nexatom Research & Instruments develops indigenous precision laser sources and scientific instruments, including the UTT810 Universal Time Tagger.">
```

Use page-specific descriptions:

- Home: company and UTT810 summary.
- Products index: current Nexatom product path.
- UTT810 product: 8-channel time tagger specifications and workflows.
- Downloads index: software downloads.
- UTT810 download: Windows installer, version, checksum.
- Achievements: precision laser and RRI milestone.
- Press: DST, Times of India, Deccan Herald coverage.
- Team: Nexatom research team.
- Contact: email and phone.
- 404: page not found.

- [ ] **Step 4: Run local static server**

Run this in a separate terminal:

```powershell
python -m http.server 8000 --directory site
```

Expected:

```text
Serving HTTP on :: port 8000
```

If port `8000` is occupied, use `8001`:

```powershell
python -m http.server 8001 --directory site
```

Open:

```text
http://localhost:8000/
http://localhost:8000/products/utt810/
http://localhost:8000/downloads/utt810/
```

Verify:

- Header navigation works.
- Product and download CTAs work.
- Nested pages load `/assets/css/styles.css`.
- No text overlap on desktop and narrow browser widths.

Stop the server with `Ctrl+C` after verification.

- [ ] **Step 5: Verify release metadata against manifest**

Run this read-only manifest check:

```powershell
python -c "import json, urllib.request; data=json.load(urllib.request.urlopen('https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json')); print(data)"
```

Expected values in the printed object:

```text
version: 1.0.1
file: Nexatom_UTT810_Setup_1.0.1.exe
size: 85,780,093
sha256: cee5a78865e0b0923649c4f922327ab54de059721135fefa8bda499ed6510e3a
```

- [ ] **Step 6: Run final verification script**

Run:

```powershell
python tools/verify_site.py
```

Expected:

```text
OK: site skeleton verified
```

- [ ] **Step 7: Inspect publish surface**

Run:

```powershell
Get-ChildItem -Recurse -Force site | Select-Object FullName
```

Expected:

- Only production website files under `site/`.
- No `docs/`, `mockups/`, `.superpowers/`, or PDF files under `site/`.

- [ ] **Step 8: Verify GitHub Pages settings before DNS cutover**

Manual acceptance checks in GitHub repository settings:

```text
Settings -> Pages -> Build and deployment -> Source: GitHub Actions
```

Expected:

- Source is `GitHub Actions`, not `Deploy from branch`.
- Latest `Deploy static site to GitHub Pages` workflow run completed successfully.
- After deployment, these URLs return 404:
  - `https://www.nexatom.in/docs/`
  - `https://www.nexatom.in/mockups/`
  - `https://www.nexatom.in/time_tagger_precision_detail_specification.pdf`
  - `https://www.nexatom.in/Nexatom_TT_Specifications%20(1).pdf`

- [ ] **Step 9: Commit final readiness pass**

Run:

```powershell
git add site tools/verify_site.py
git commit -m "Finalize static site metadata and verification"
```

---

## Self-Review Checklist

- Spec coverage: homepage, UTT810 product, UTT810 download, achievements, press, team, contact, deployment boundary, metadata, and verification are covered by tasks.
- Publish boundary: production files live in `site/`; GitHub Actions deploys only `site/`.
- Download separation: installer, release, and manifest remain in `nexatom-downloads` / `downloads.nexatom.in`; website links out only.
- Product claims: `<10 ps` timing jitter is labeled as specification; validation wording includes setup uncertainty.
- Link strategy: internal links are root-relative.
- Scaffold pages: Task 1 creates minimal pages only to establish deployable structure; later tasks replace them with content-specific pages before launch readiness.
