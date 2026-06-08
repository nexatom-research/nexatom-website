# AGENTS.md

This repository is the planned static website for Nexatom Research & Instruments.

Scope: Entire repository.

## Repository Purpose

- GitHub repo: `nexatom-research/nexatom-website`
- Local checkout: `F:\vscode_projects\nexatom-website`
- Goal: replace the current Google Sites website with a GitHub Pages static site.
- Target public site: `https://www.nexatom.in`
- Keep the software updater/download infrastructure separate from this repo.

## Important Separation

Do not merge the website repo with the Flutter app repo or the downloads repo.

- Flutter app repo:
  `F:\vscode_projects\zynq_tt_library_and_gui\zynq_tt_ftdi_nexatom_gui`
- Native/API repo:
  `F:\vscode_projects\zynq_tt_library_and_gui\native_API_library_sync_clk`
- Downloads/updater repo:
  `nexatom-research/nexatom-downloads`
- Website repo:
  `nexatom-research/nexatom-website`

The app updater already depends on:

`https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json`

Do not break or move that URL. The website may link to downloads, but updater manifests and installer assets remain owned by `nexatom-downloads`.

## Current Public Website Context

The existing website is built with Google Sites and is bare-bones. The visible navigation is:

- Home
- Downloads, nested under Home
- Team
- Achievements
- Press Coverage
- Contact

Known current content:

- Home: company positioning around nexAtom, "Let's build together", About Us, Problem and Solution, Portfolio, Closer Look, contact email/phone, and LinkedIn.
- Downloads: only a Google Drive software link with typo: "Click to Downlaod Software for Nexatom UTT 810".
- Team: short team description.
- Achievements: precision laser system, dual-channel tunable lasers, and RRI license agreement milestone.
- Press Coverage: DST, Times of India, and Deccan Herald references.
- Contact: email and phone.

Primary content gap: there is no proper product page for UTT810, even though the app installer and updater now exist.

## Recommended First Site Structure

Use plain static HTML/CSS first. Avoid a framework until there is a real maintenance need.

Suggested structure:

```text
nexatom-website/
  index.html
  products/
    utt810/
      index.html
  downloads/
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
```

## GitHub Pages Plan

Use GitHub Pages "Deploy from branch" initially:

- Branch: `main`
- Folder: `/`
- Static files only

Add a `CNAME` file containing:

```text
www.nexatom.in
```

Later, in GitHub repository settings:

- Enable Pages.
- Set custom domain to `www.nexatom.in`.
- Enable HTTPS after DNS resolves.

## DNS Plan

DNS must be changed wherever `nexatom.in` is managed.

Current known DNS state from prior inspection:

- `www.nexatom.in` points to Google Sites via `ghs.googlehosted.com`.
- `nexatom.in` apex currently has an `A` record to `198.185.159.144`.
- `downloads.nexatom.in` already points to `nexatom-research.github.io`.
- Existing Zoho TXT/SPF records exist and must not be touched.

Planned records:

```text
www  CNAME  nexatom-research.github.io
```

For apex/root `nexatom.in`, use GitHub Pages A records if serving or redirecting apex:

```text
@  A  185.199.108.153
@  A  185.199.109.153
@  A  185.199.110.153
@  A  185.199.111.153
```

Optional IPv6:

```text
@  AAAA  2606:50c0:8000::153
@  AAAA  2606:50c0:8001::153
@  AAAA  2606:50c0:8002::153
@  AAAA  2606:50c0:8003::153
```

Do not configure wildcard DNS like `*.nexatom.in`.

## Downloads Page Requirements

The user still needs a manual first install before auto-update can work.

The website should provide:

- A clear "Download for Windows" button for Nexatom UTT810 Time Tagger.
- Latest version.
- File size.
- SHA256 checksum.
- Short note: "After first install, future updates are available inside the app."
- Support/contact path for installation issues.

Current release metadata:

- Release repo: `nexatom-research/nexatom-downloads`
- Release tag: `time-tagger-UTT810-v1.0.1`
- Release page: `https://github.com/nexatom-research/nexatom-downloads/releases/tag/time-tagger-UTT810-v1.0.1`
- Installer URL:
  `https://github.com/nexatom-research/nexatom-downloads/releases/download/time-tagger-UTT810-v1.0.1/Nexatom_UTT810_Setup_1.0.1.exe`
- Updater manifest:
  `https://downloads.nexatom.in/apps/time-tagger/UTT810/latest.json`

Prefer linking users to a website download page:

`https://www.nexatom.in/downloads/utt810/`

The download page can link to the GitHub Release installer asset or read/display metadata from `latest.json`.

## First Implementation Priorities

1. Create a professional but simple static website.
2. Preserve the current pages so existing visitors are not confused.
3. Add a dedicated `Products / UTT810` page.
4. Replace Google Drive software download with the release-backed installer flow.
5. Add checksum/version/update-note details.
6. Keep the visual style clean, credible, and instrumentation-focused.

## Suggested First Page List

- Home
- Products / UTT810
- Downloads / UTT810
- Achievements
- Press
- Team
- Contact

## Working Style

- Keep the site static unless the user explicitly asks for a framework.
- Prefer readable HTML/CSS over generated complexity.
- Keep copy concrete and product-focused.
- Avoid overbuilding forms, CMS, or backend features in the first pass.
- Do not touch DNS from code. DNS changes must be made deliberately by the user or with explicit confirmation.

