# Architectural Decisions — mlpartnersllc.com

## 2026-06-11 — Self-hosted SES relay for the contact form
Instead of a third-party form service (Formspree etc.) or exposing a mailto link, the form posts to a tiny stdlib-Python service on localhost that sends via the AWS SES account already configured for the domain's email. Reasons: no new vendor, no exposed email address for scrapers, reuses verified SES identity, and spam control stays local (honeypot + app rate limits + nginx `limit_req`). The service is deliberately stdlib-only (plus boto3) so it has no framework dependencies to maintain.

## 2026-06-11 — Drop Bootstrap for a custom CSS design system
The redesigned "grid at night" aesthetic (HUD panels, mono telemetry type, canvas map) shares almost nothing with Bootstrap's component model. Bootstrap 5.3 + Popper were removed from both `package.json` and the CDN links; all styling now lives in `BaseLayout.astro` design tokens plus component-scoped styles. This cut page weight (no 200KB+ framework CSS/JS) and removed the generic look.

## 2026-06-11 — Canvas-generated map instead of an image
The hero "satellite night view of the USA" is generated at runtime in `NightGrid.astro` from embedded simplified lon/lat polygons + a weighted city list, rather than a licensed NASA photo. Reasons: no image licensing, crisp at every DPI/viewport, MISO footprint can be styled independently (amber vs. cool dots), and transmission pulses can animate along the same geometry. A seeded RNG keeps renders deterministic. Static dots are pre-rendered to an offscreen layer; only ~400 twinkles + ~27 pulses redraw per frame. `prefers-reduced-motion` gets a static frame.

## 2026-06-11 — Positioning: proprietary trader, not a service firm
All site copy is written from the standpoint of a prop desk trading its own capital ("No clients. No fund. No services for sale."). Any future content must not solicit consulting work.

## 2026-06-11 — Stylized geography with disclaimer
US outline, Great Lakes, MISO footprint, and hub locations are simplified/stylized. The footer carries "Map visualization is stylized & illustrative — not live grid data" to avoid implying real-time market data.
