# Ethembeni Foundation — website

Static site (HTML, CSS, vanilla JS). No build step. Netlify builds `main`
automatically on every push; the publish directory is the repo root.

## Editing

- `index.html` — all page content
- `style.css` — all styling, including the phone/tablet/desktop breakpoints
- `script.js` — mobile menu, scroll-spy, reveal animation, footer year
- `assets/` — images, logo, partner marks and the social icons (PNG)

## Checks before pushing

- Every `src`/`href` that points at a local file must exist with the exact
  same letter case — Netlify runs Linux and is case-sensitive.
- Section `.reveal` elements are hidden only when JavaScript is running, so
  the page still renders if scripts are blocked.
- Social icons are PNG `<img>` files on purpose: Chromium-based browsers
  (Brave, Chrome, Edge) will not paint `<use>` references into a zero-sized
  SVG sprite, which made the row disappear on phones.

## Never commit

`_shot.html`, `_diag.html`, `_diag.py` and other scratch files are listed in
`.gitignore`. They were published once by accident; keep them out.
