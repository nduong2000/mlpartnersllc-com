# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ML Partners LLC company website - a professional business landing page built with Astro and Bootstrap.

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
