# ML Partners, LLC Website

Professional business landing page built with Astro and Bootstrap.

## Development Commands

```bash
npm run dev      # Start dev server (http://localhost:4321)
npm run build    # Build for production (outputs to dist/)
npm run preview  # Preview production build locally
```

## Architecture

**Tech Stack:** Astro 5.x + Bootstrap 5.3 (via CDN)

**Structure:**
- `src/layouts/BaseLayout.astro` - Main HTML layout with Bootstrap CSS/JS imports
- `src/components/` - Reusable components (Navbar, Footer)
- `src/pages/index.astro` - Landing page with hero, services, about, contact sections
- `src/pages/contact.astro` - Dedicated contact page
- `public/` - Static assets (favicon)
- `dist/` - Build output (static HTML)

**Styling:** Global styles in BaseLayout.astro, component-scoped styles using `<style>` tags. Bootstrap loaded via CDN, Bootstrap Icons via CDN.

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

**Forwarding:** AWS SES forwards to duong.nick@gmail.com

**Setup:**
- Domain verified in AWS SES (us-east-1)
- DKIM enabled
- MX record: `10 inbound-smtp.us-east-1.amazonaws.com`
- Lambda forwarder: `SESEmailForwarder`
- Receipt rule set: `mlpartnership-email-rules`
