# Nexatom Website First Pass Design

Date: 2026-06-08

## Purpose

Build the first static GitHub Pages version of the Nexatom Research & Instruments website at `https://www.nexatom.in`.

The site should preserve the current company-first public story while adding a strong product and download path for the Nexatom UTT810 Universal Time Tagger. The result should feel credible for scientific instrumentation buyers, researchers, and technical partners without overbuilding a CMS, backend, or app-like framework.

## Decisions Already Approved

- Keep the site static: plain HTML and CSS first.
- Preserve the current company-first structure and story from the live Google Sites website.
- Add UTT810 as a strong featured product path, not as the sole homepage focus.
- Homepage direction: company hero with visible UTT810 CTAs and a featured product strip.
- UTT810 product page direction: product story plus spec highlights, applications, feature sections, and grouped specs.
- UTT810 download page direction: installer card with version, file size, SHA256, update note, and support contact.
- First visual direction: technical HTML/CSS visuals and diagrams. Replace or augment with owned images later.
- Do not scrape or depend on opaque Google Sites image URLs.
- Do not gate the installer behind a form.
- Do not move updater manifests or installer assets into this repo.
- Treat the current local PDFs, planning docs, and mockups as design inputs, not automatically public website assets.

## Repository Boundaries

This repo owns the public static website only.

Keep separate:

- Website repo: `nexatom-research/nexatom-website`
- Downloads/updater repo: `nexatom-research/nexatom-downloads`
- Flutter app repo: `F:\vscode_projects\zynq_tt_library_and_gui\zynq_tt_ftdi_nexatom_gui`
- Native/API repo: `F:\vscode_projects\zynq_tt_library_and_gui\native_API_library_sync_clk`

The website may link to the installer and release metadata, but must not move or alter the updater URL:

`https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json`

## Site Structure

Use this static structure:

```text
nexatom-website/
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
    images/
    js/
  CNAME
  .nojekyll
  404.html
  robots.txt
  sitemap.xml
```

`assets/js/` can remain empty unless a small progressive enhancement is useful. The first pass should not require JavaScript to display core content or downloads.

`404.html`, `robots.txt`, and `sitemap.xml` can be minimal in the first pass, but they should exist for basic GitHub Pages polish.

## Publication Boundary

GitHub Pages deploys every committed file under the configured publish root. If Pages is configured as `main` branch, folder `/`, then root-level PDFs, `docs/`, `mockups/`, and planning artifacts can become publicly reachable even if they are not linked.

Before enabling Pages from `/`, choose one publication model:

1. Keep only production-safe website files committed under the root deploy tree.
2. Move internal specs, mockups, and source PDFs outside the deploy tree before launch.
3. Switch to a dedicated public deploy folder or GitHub Actions publish flow if planning documents must remain committed in this repo.

Do not publish the local UTT810 PDFs unless Nexatom explicitly approves them as public-facing files.

## Navigation

Primary navigation:

- Home
- Products
- Downloads
- Achievements
- Press
- Team
- Contact

`Products` should link directly to `products/utt810/` in the first pass. Later, if Nexatom adds more products, this can become a product index page.

`Downloads` should link directly to `downloads/utt810/` in the first pass. Later, this can become a downloads index if more products need public software support.

Also add lightweight index pages at `/products/` and `/downloads/` so direct visitors and search engines do not hit 404s. Each index can list the UTT810 page as the current public product/download.

Use root-relative internal URLs for production:

- `/`
- `/products/`
- `/products/utt810/`
- `/downloads/`
- `/downloads/utt810/`
- `/achievements/`
- `/press/`
- `/team/`
- `/contact/`
- `/assets/css/styles.css`

This avoids broken paths from nested pages.

## Homepage

The homepage remains company-first.

Content goals:

- Preserve the current Nexatom positioning around indigenous precision laser sources and scientific instruments.
- Keep the current themes: "Let's build together", About Us, Problem and Solution, Portfolio, Closer Look, and contact path.
- Preserve the LinkedIn path currently shown on the live homepage, using the final approved LinkedIn URL/text.
- Add a visible UTT810 product path near the top without making the homepage product-only.

Recommended page flow:

1. Header and navigation.
2. Company hero:
   - Brand: `nexAtom`
   - Primary message: indigenous precision laser sources and scientific instruments.
   - Supporting copy: research-to-product translation for research and industry.
   - CTAs: `Explore UTT810` and `Download Software`.
3. Featured UTT810 strip:
   - `Nexatom UTT810 Universal Time Tagger`
   - Short positioning line.
   - Metric tiles: 8 channels, 1 ps time bin width, timing jitter specification, USB 3 / data transfer.
4. About Us.
5. Problem and Solution.
6. Portfolio / Closer Look.
7. Achievements and press credibility teasers.
8. Contact callout.

## UTT810 Product Page

The product page should be technical and readable, not a PDF dump.

Primary audience:

- Researchers evaluating time-tagging hardware.
- Quantum optics and spectroscopy users.
- Lab teams who need coincidence, histogram, correlation, and synchronized timing workflows.
- Existing or prospective UTT810 users looking for software/download/support paths.

Recommended page flow:

1. Product hero:
   - `Nexatom UTT810 Universal Time Tagger`
   - One-line positioning: an 8-channel USB time tagger for coincidence, histogram, correlation, and synchronized event-timing measurements.
   - CTAs: `Download Software`, `Contact Nexatom`, and optionally `View Specifications`.
2. Metric highlights:
   - 8 input channels.
   - 1 ps time bin width.
   - `<10 ps` timing jitter specification.
   - 4 ns dead time.
   - USB 3 data transfer above 300 MB/s.
   - GUI and API with absolute time-tag saving.
3. Applications:
   - Relevant workflows include coincidence counting.
   - Quantum optics experiments.
   - Spectroscopy and time-correlated measurements.
   - Correlation measurements.
   - Multi-channel event timing.
   - Synchronized instrument timing.
4. Feature sections:
   - Real-time FPGA time histogram with minimum 1 ps bin width and multi-stop support.
   - Real-time multi-fold coincidence histogram up to 8 channels.
   - Real-time linear and multi-tau correlation measurement with auto/cross modes.
   - Input threshold and hysteresis controls.
   - External 10 MHz TTL synchronization support.
   - GUI and API workflow.
5. Grouped specification table:
   - Timing.
   - Channels.
   - Input signals.
   - Processing.
   - Interface.
   - Software.
   - Synchronization.
6. Validation note:
   - Mention measured timing performance carefully.
   - Avoid presenting validation setup uncertainty as pure device-only jitter.
7. Final CTA:
   - Download Windows software.
   - Contact for quotes/support.

## UTT810 Specification Claims

Use claims from the local PDFs:

- Model: Nexatom Universal Time Tagger, model `UTT_810` / UTT810.
- Channels: 8.
- Time bin width: 1 picosecond.
- Timing jitter: `< 10 picoseconds`.
- Dead time: 4 nanoseconds.
- Maximum data processing: up to 125 million combined events, as specified in product documentation. Do not present this as events per second unless confirmed.
- Time histogram: real-time FPGA processing, minimum 1 ps bin width, multi-stop.
- Coincidence histogram: real-time multi-fold histogram up to 8 channels.
- Correlation: real-time linear and multi-tau, minimum 8 ns bin width, auto/cross.
- Input hysteresis: 1 mV to 100 mV on all input channels.
- Input voltage range: 0 to 5 V.
- Input pulse delay: 1 ps to 4 ns physical delay.
- Input threshold voltage: 0 to 2.5 V, 1 mV step.
- Input impedance: 50 ohms.
- Data transfer: above 300 MB/s on USB 3.
- Software: GUI and API available with absolute time-tag saving.
- External sync: 10 MHz TTL clock signal on GPIO pin 2; GUI detects valid clock when `Use External Sync` is enabled.

Separate device specification claims from internal validation measurements.

Device/specification copy may say:

- 1 ps time bin width.
- `<10 ps` timing jitter specification.

Internal validation copy should be cautious:

> Internal two-channel validation showed an effective single-channel contribution of 24.5 ps FWHM / 10.5 ps RMS in the test setup, including signal source and measurement-chain uncertainty.

Avoid:

- Treating 1 ps bin width as 1 ps accuracy.
- Presenting validation uncertainty as pure device-only jitter.
- Placing `<10 ps` timing jitter and `24.5 ps FWHM` validation language next to each other without labels that explain the difference.
- Saying "best", "world-class", or similar unless supported by a clear public benchmark.

## Downloads / UTT810 Page

The download page should replace the current Google Drive link and typo with a release-backed installer flow.

Primary content:

- Page title: `Nexatom UTT810 Time Tagger Software`
- Primary CTA: `Download for Windows`
- Version: `1.0.1`
- File: `Nexatom_UTT810_Setup_1.0.1.exe`
- File size: `85,780,093` bytes, displayed as `85.78 MB`
- SHA256: `cee5a78865e0b0923649c4f922327ab54de059721135fefa8bda499ed6510e3a`
- Installer URL:
  `https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.1/Nexatom_UTT810_Setup_1.0.1.exe`
- Release page:
  `https://github.com/nexatom-research/nexatom-downloads/releases/tag/time-tagger-UTT810-v1.0.1`
- Updater manifest, shown only as technical metadata:
  `https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json`

The static page displays the pinned release metadata at implementation time. Whenever `latest.json` changes for a new UTT810 release, manually update the website download page in the same release process or run a verification checklist that compares the page metadata against the manifest.

Do not require runtime JavaScript fetching for the download page's core content.

Required note:

> After first install, future updates are available inside the app.

Support path:

- `nexatom.research@gmail.com`
- `+91 8884998660`

The page should make the direct installer button obvious. GitHub release and manifest links should be secondary.

## Other Pages

### Achievements

Preserve the current achievement topics:

- Precision laser system.
- Ultra-stable, high-precision, dual-channel tunable lasers.
- Custom powers, form factors, and integration solutions.
- RRI license agreement milestone with Raman Research Institute, Bangalore and Nexatom Research and Instruments Pvt. Ltd.
- Quantum and spectroscopy application framing.

Use owned media later if available. Do not scrape Googleusercontent images for production.

### Press

Preserve the current press references:

- DST recognition.
- Times of India coverage.
- Deccan Herald coverage.

Use text summaries and outbound links. Avoid embedding third-party logos or article screenshots unless Nexatom has usage rights.

Preserve a cleaned-up version of the current press-page disclaimer that trademarks, logos, brand names, and article ownership belong to their respective owners, and that references are for informational/coverage purposes.

### Team

Preserve the current team positioning:

- Highly talented, tenacious researchers.
- Coalition of experts translating high-tech lasers, laser-based instruments, and cutting-edge technology into tangible applications.

This page can remain brief in the first pass unless final team member bios/photos are provided.

### Contact

Preserve:

- `nexatom.research@gmail.com`
- `+91 8884998660`
- Approved LinkedIn profile/company URL and label.

Do not build a contact form in the first pass.

## Visual Direction

First pass uses technical HTML/CSS visuals:

- Instrument front-panel style hero for UTT810.
- Timing pulse traces.
- 8-channel input visual.
- Metric tiles.
- Coincidence peak diagram.
- FPGA processing pipeline.
- External sync diagram.
- Download verification panel.

Use owned images later where they improve trust:

- Logo/source brand assets.
- Product photos.
- GUI screenshots.
- Lab or instrument media.
- RRI/license event photos if approved for public use.

Production should not depend on the temporary `.superpowers/` companion files.

## Deployment

Use GitHub Pages "Deploy from branch":

- Branch: `main`
- Folder: `/`

Add:

- `CNAME` containing `www.nexatom.in`
- `.nojekyll`

Deployment acceptance checks:

- `www.nexatom.in` resolves to GitHub Pages after DNS is changed.
- HTTPS is enabled after DNS settles.
- `downloads.nexatom.in/apps/time-tagger/UTT810/latest.json` remains unchanged and reachable.
- Apex `nexatom.in` behavior is deliberately chosen: either GitHub Pages apex support or a deliberate redirect/parking choice.
- No wildcard DNS such as `*.nexatom.in` is configured.

DNS changes are outside code and must be done deliberately by the user. Do not modify DNS from this repository.

## Testing And Verification

Before implementation is considered complete:

- Open the static pages locally in a browser.
- Serve the site through a local static HTTP server and test through `http://localhost`, not only `file://`.
- Verify navigation links work from every page.
- Verify root-relative internal paths work under nested pages.
- Verify the download button points to the GitHub release installer asset.
- Verify the release page and manifest links are visible but secondary.
- Verify no production page links to the old Google Drive download.
- Verify the SHA256 value matches the live manifest.
- Verify the visible version, file size, SHA256, and installer URL match `latest.json` for the pinned release.
- Crawl internal links and check obvious external links.
- Run an HTML validation pass or equivalent structural check.
- Inspect the publish root for accidental public files: internal PDFs, `docs/`, `.superpowers/`, mockups, local notes, and unrelated repo artifacts.
- Verify `404.html`, `robots.txt`, `sitemap.xml`, favicon/brand icons, and basic page metadata exist or are deliberately deferred.
- Check desktop and mobile responsive layouts.
- Check text does not overlap or overflow in buttons, metric cards, tables, and nav.

## Open Items For User Review

- Confirm final brand spelling/casing: `nexAtom`, `Nexatom`, or mixed by context.
- Provide owned logo/product/media assets when ready.
- Confirm whether to display the local PDF specs as downloadable public files or keep them internal for copy only.
- Confirm whether the UTT810 PDFs may be treated as public-facing source material.
- Confirm exact public wording for timing jitter, timing resolution, and validation results.
- Confirm what "up to 125 million combined events" means before using it in prominent marketing copy.
- Confirm final release date format if the download page should show a release date.
- Confirm whether a `Request quote` CTA should appear on the product page.
