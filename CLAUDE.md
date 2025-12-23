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
- `public/` - Static assets (favicon)
- `dist/` - Build output (static HTML)

**Styling:** Global styles in BaseLayout.astro, component-scoped styles using `<style>` tags. Bootstrap loaded via CDN, Bootstrap Icons via CDN.

**Build:** Static site generation - no server required for deployment.

## Deployment

**Production URL:** https://mlpartnersllc.com

**Server:** OpenResty/nginx reverse proxy to Astro dev server

**Nginx Config:** `/usr/local/openresty/nginx/conf/conf.d/mlpartnersllc.com.conf`

**SSL:** Let's Encrypt certificate via certbot (auto-renews)

### Deploying Changes
1. Changes to Astro files are hot-reloaded (dev server running in background)
2. To restart dev server: `npm run dev --host 0.0.0.0`
3. Nginx config changes: copy from `nginx/` and reload OpenResty:
   ```bash
   sudo cp nginx/mlpartnersllc.com.conf /usr/local/openresty/nginx/conf/conf.d/
   sudo systemctl reload openresty
   ```
