# ML Partners, LLC Website

Landing page for ML Partners, LLC — a proprietary energy trading firm (MISO market participant since 2008). Dark "satellite night view / power grid" design built with Astro and custom CSS (no CSS framework).

**Positioning:** ML Partners is an energy trader, NOT a services/consulting company. Copy must never pitch services or solicit clients — the firm trades its own book.

## Development Commands

```bash
npm run dev      # Start dev server (http://localhost:4321)
npm run build    # Build for production (outputs to dist/)
npm run preview  # Preview production build locally
```

## Architecture

**Tech Stack:** Astro 5.x + hand-written CSS design system (no Bootstrap — removed in the 2026-06 redesign)

**Structure:**
- `src/layouts/BaseLayout.astro` - HTML layout + global design tokens/CSS (fonts, buttons, panels, ticker, reveal animations)
- `src/components/Navbar.astro` - Fixed nav with EST "grid clock" and mobile toggle
- `src/components/Footer.astro` - Footer with disclaimer that the map is stylized
- `src/components/NightGrid.astro` - Canvas hero: lower-48 as satellite night lights; MISO footprint glows amber, non-MISO dots cool white; animated transmission pulses between stylized MISO hubs; respects `prefers-reduced-motion`
- `src/pages/index.astro` - Landing page: hero, ticker, The Desk / The Edge / The Footprint / The Record / Contact
- `src/pages/contact.astro` - Contact form page (posts JSON to `/api/contact`)
- `server/contact_api.py` - Contact form backend: stdlib HTTP server on `127.0.0.1:8826`, relays submissions to `nduong@mlpartnersllc.com` via AWS SES (boto3, us-east-1). Honeypot field + per-IP (5/hr) and global (50/day) rate limits
- `server/mlpartners-contact.service` - systemd unit for the contact API (copy to `/etc/systemd/system/` and enable)
- `public/` - Static assets (favicon)
- `dist/` - Build output (static HTML) — **served directly by nginx; `npm run build` deploys to production**

**Contact form flow:** browser form → nginx `location = /api/contact` (rate-limited via `contact_form` zone, proxies to 127.0.0.1:8826) → `contact_api.py` → SES `send_email` (From: nduong@mlpartnersllc.com, Reply-To: submitter) → SES inbound → Lambda forwarder → Gmail. No email addresses are exposed in page markup.

**Design system:** Dark night palette (`--night #050910`), amber city-light accent (`--amber #ffb454`), cool blue secondary. Fonts: Archivo variable (expanded-width display headlines) + IBM Plex Mono (telemetry/labels), both via Google Fonts. HUD-style panels with corner ticks, mono uppercase eyebrows, film-grain overlay.

**Map geometry:** `NightGrid.astro` embeds simplified lon/lat polygons (US outline hugging the US shore of the Great Lakes, Lake Michigan hole, stylized MISO footprint) with a deterministic seeded RNG so renders are reproducible. Footer carries an "illustrative, not live grid data" disclaimer.

**Build:** Static site generation - no server required for deployment.

## Deployment

**Production URL:** https://mlpartnersllc.com

**Server:** OpenResty/nginx serving static files from `dist/`

**Nginx Config:** `/usr/local/openresty/nginx/conf/conf.d/mlpartnersllc.com.conf`

**SSL:** Let's Encrypt certificate via certbot (auto-renews)

### Deploying Changes
1. Build the static site:
   ```bash
   npm run build
   ```
2. Nginx serves from `dist/` automatically - no restart needed for content changes
3. For nginx config changes:
   ```bash
   sudo cp nginx/mlpartnersllc.com.conf /usr/local/openresty/nginx/conf/conf.d/
   sudo systemctl reload openresty
   ```

## Email

**Contact Email:** nduong@mlpartnersllc.com

**Gmail Integration:** duong.nick@gmail.com (send and receive as nduong@mlpartnersllc.com)

### DNS Records (DNSexit)
| Type | Name | Value |
|------|------|-------|
| MX | `@` | `10 inbound-smtp.us-east-1.amazonaws.com` |
| TXT | `@` | `v=spf1 include:amazonses.com ~all` |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:nduong@mlpartnersllc.com` |
| TXT | `_amazonses` | SES verification token |
| CNAME | `*._domainkey` | DKIM records (3 entries for SES) |

### Receiving (AWS SES → Gmail)
- Domain verified in AWS SES (us-east-1)
- DKIM enabled (3 CNAME records)
- Lambda forwarder: `SESEmailForwarder`
- Receipt rule set: `mlpartnership-email-rules`
- S3 bucket stores raw emails before forwarding

**Lambda Forwarder Behavior:**
- From: `Nick Duong <nduong@mlpartnersllc.com>` (SES requirement)
- Reply-To: Original sender's address
- Subject: Preserved from original email
- Attachments: Supported

**Forward Mapping:**
- `nduong@mlpartnersllc.com` → `duong.nick@gmail.com`
- `nduong@mlpartnership.com` → `duong.nick@gmail.com`
- `admin@mlpartnership.com` → `duong.nick@gmail.com`

### Sending (Gmail → AWS SES SMTP)
Gmail "Send mail as" configured with AWS SES SMTP:
- SMTP Server: `email-smtp.us-east-1.amazonaws.com`
- Port: `587` (TLS)
- IAM User: `ses-smtp-mlpartnersllc`
- Credentials stored in Gmail settings
- Reply-To: `nduong@mlpartnersllc.com`

**Gmail Setup:** Settings → Accounts and Import → Send mail as → nduong@mlpartnersllc.com

### Authentication Status
- SPF: pass
- DKIM: pass
- DMARC: pass

**Note:** New domains may initially trigger spam filters on Yahoo/others. Add sender to contacts and mark as "Not Spam" to train filters.
