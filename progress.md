# Progress — mlpartnersllc.com

## 2026-06-23 — Encrypted upload page (/contactme.html) + shared :8082 backend fix

- Copied `localupload2.html` from mlpartnership.com into `public/`, then renamed to `contactme.html` (live at https://mlpartnersllc.com/contactme.html; old `/localupload2.html` 404s). In-browser age encryption (X25519 + ChaCha20-Poly1305) via self-hosted `public/js/age-bundle.js` (SRI-verified, no WASM so existing CSP is fine); uploads only ciphertext.
- Added `public/css/styles.css` (from mlpartnership.com) for navbar/footer chrome; branding rebranded to "ML Partners, LLC", navbar → `/`.
- nginx: added `location = /upload-encrypted-raw` proxy → 127.0.0.1:8082 (200M cap, Authorization/X-Filename pass-through, 60s timeouts) to `nginx/mlpartnersllc.com.conf` + live conf; reloaded.
- **Backend fix (shared infra):** the running `:8082` server (`mlp-upload.service` → `/usr/share/nginx/mlpartnership-html/upload-server.js`) was an older build lacking `/upload-encrypted-raw` → returned 405 on BOTH sites. The repo build with the endpoint (`upload-server.service`) was crash-looping (194k restarts, port conflict). Fix: backed up + swapped the deployed file to the repo superset, restarted `mlp-upload.service`, disabled `upload-server.service`. Verified bad-token POST now → 401 (was 405) direct, via mlpartnersllc.com, and via mlpartnership.com. See bugs.md.

## 2026-06-11 — Footer link + win-rate copy removal

- Footer: removed the external "Dashboard ↗" (mlpartnership.com/miso) and "GitHub ↗" links; footer now only has internal section links + Contact.
- Landing page: removed the 70.5% win-rate claim everywhere — the Price Forecasting panel sentence now ends "…sits behind every position the desk takes," and the hero stat "70.5% Directional Win Rate" was replaced with "623K Transmission Graph Edges" (kept the 4-column stat grid).
- Hero "Live Dashboard ↗" CTA (mlpartnership.com/miso) removed per follow-up; replaced with a ghost "Contact the Desk" button → `/contact`. Site now has zero references to the dashboard, GitHub, or LinkedIn.
- Rebuilt; verified no "70.5" and no footer external links in `dist/`.

## 2026-06-11 — Contact form replaces exposed email/channel links

- Removed the contact-page channel cards (Email/GitHub/LinkedIn/Dashboard) and all visible email addresses/mailto links; homepage contact CTA now links to `/contact`.
- New contact form (name/email/message) posts to `/api/contact`; styled to match the HUD design (amber focus glow, mono labels, "Transmitted" success panel).
- Backend: `server/contact_api.py` (stdlib HTTP + boto3 SES, port 8826 localhost-only) — honeypot, validation, per-IP 5/hr + global 50/day rate limits; SES From `nduong@mlpartnersllc.com`, Reply-To submitter.
- nginx: `limit_req_zone contact_form` (3 r/min, burst 5) + `location = /api/contact` proxy added to `nginx/mlpartnersllc.com.conf` and deployed (synced stale repo copy from live conf first — repo copy had old root path and was missing fmprep blocks).
- Per user request, removed The Edge tech paragraph (HTTP/2/DuckDB/MLflow copy) and the tech chip row from the landing page.
- Verified end-to-end: honeypot fake-success, validation 400s, real SES send delivered (log: "sent contact mail").
- **Pending:** contact API currently runs via nohup; systemd install blocked by permissions. To persist: `sudo cp server/mlpartners-contact.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now mlpartners-contact`.

## 2026-06-11 — Full redesign: "grid at night" trading-desk site

- Repositioned all copy: ML Partners is a **proprietary energy trader** (MISO participant since 2008), not a services company. Removed all "hire us" / services language.
- New dark aesthetic: NASA-satellite-night-view of the lower 48 as the hero — canvas-rendered city lights (amber inside the MISO footprint, cool white outside), animated transmission pulses between stylized MISO hub markers (MINN.HUB, INDIANA.HUB, etc.), dashed footprint boundary.
- New page structure: Hero → hub ticker → 01 The Desk (virtual trading, LSTM forecasting, congestion analytics) → 02 The Edge (in-house stack + stats) → 03 The Footprint (MISO facts) → 04 The Record (registry-style panel, since 2008, clean record) → 05 Contact.
- Removed Bootstrap + Popper entirely (deps and CDN links); replaced with a hand-written design system in `BaseLayout.astro` (Archivo expanded display + IBM Plex Mono, HUD panels with corner ticks, film grain, reveal-on-scroll).
- Navbar: EST "grid clock" (MISO market time, no DST), blinking status dot, custom mobile menu.
- Contact page rebuilt to match; states explicitly the firm takes no clients/outside capital.
- New favicon (amber node constellation on night background).
- Verified: polygon membership tests (cities in/out of US, lakes, MISO region) pass in Node; production nginx returns 200 with new content.
- Backup of previous live dist: `/mnt/ssd/backup/mlpartnersllc-dist-20260611-*.tar.gz`.
- Not yet committed to git (awaiting go-ahead).
