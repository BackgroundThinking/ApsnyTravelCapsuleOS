> # ApsnyTravelCapsuleOS - Deployment & Operations Guide

**Version:** 1.0
**Date:** December 2, 2025

---

## 1. Introduction

This guide provides comprehensive instructions for deploying, configuring, and maintaining the ApsnyTravelCapsuleOS application. The project is a static web application built with React, Vite, and a custom Python-based content compiler, designed for high performance and easy maintenance.

### 1.1. Architecture Overview

- **Frontend:** Vite + React 19 + TypeScript SPA
- **Styling:** Tailwind CSS 4 + shadcn/ui
- **Content Layer:** Markdown capsules compiled into a static JSON API (`capsules.json`)
- **Build System:** `pnpm` for dependencies, Vite for bundling, and Python for content compilation

---

## 2. Prerequisites

Ensure the following software is installed on your local machine or CI/CD environment:

- **Node.js:** `v18.0` or higher
- **pnpm:** `v10.0` or higher
- **Python:** `v3.11` or higher

### 2.1. Verifying Installation

```bash
node -v
pnpm -v
python3 --version
```

---

## 3. Configuration

### 3.1. Environment Variables

Create a `.env` file in the project root to configure environment variables. These are primarily for analytics and optional integrations.

```env
# Base URL for the deployed site (used for sitemap generation)
VITE_BASE_URL=https://apsnytravel.com

# Umami Analytics (Optional)
VITE_ANALYTICS_ENDPOINT=https://analytics.example.com/umami.js
VITE_ANALYTICS_WEBSITE_ID=your-website-id
```

### 3.2. Sitemap Configuration

The base URL for the sitemap is configured in `generate_sitemap.py`. It defaults to `https://apsnytravel.com` but can be overridden via command-line argument or by editing the script.

---

## 4. Build Process

The build process is fully automated and handles all necessary steps to prepare the application for deployment.

### 4.1. Build Command

To build the application, run the following command from the project root:

```bash
pnpm build
```

This command executes the following steps:

1.  **`python3 generate_sitemap.py`**: Generates `sitemap.xml`, `robots.txt`, and `sitemap-index.xml`.
2.  **`vite build`**: Compiles the React application, bundles assets, and performs code splitting.
3.  **`esbuild server/index.ts`**: Compiles the Node.js server (for optional server-side features).

### 4.2. Build Output

The entire static application will be generated in the `dist/public` directory. This directory is ready for deployment to any static hosting provider.

---

## 5. Deployment

The application is designed for static deployment, which offers the best performance, security, and scalability.

### 5.1. Recommended Providers

- **Vercel:** Excellent for Next.js/React projects, with seamless Git integration and global CDN.
- **Netlify:** Similar to Vercel, with a strong focus on static sites and serverless functions.
- **AWS S3 + CloudFront:** A robust, scalable solution for hosting static assets with a global CDN.
- **GitHub Pages:** A free and simple option for public repositories.

### 5.2. Vercel Deployment Example

1.  **Push to GitHub:** Ensure your code is pushed to a GitHub repository.
2.  **Import Project:** In your Vercel dashboard, import the GitHub repository.
3.  **Configure Build Settings:**
    - **Framework Preset:** `Vite`
    - **Build Command:** `pnpm build`
    - **Output Directory:** `dist/public`
    - **Install Command:** `pnpm install`
4.  **Add Environment Variables:** Add the contents of your `.env` file to the Vercel project settings.
5.  **Deploy:** Vercel will automatically build and deploy the application.

### 5.3. Manual Deployment

To deploy manually, simply upload the contents of the `dist/public` directory to your hosting provider's file storage.

---

## 6. Content Management

Content is managed through Markdown files (capsules) located in the (currently conceptual) `ApsnyTravelCatalog` repository or a local `capsules/` directory.

### 6.1. Content Workflow

1.  **Add/Edit Capsules:** Create or modify `.md` files in the content directory.
2.  **Update `capsules.json`:** The `capsules.json` file is the single source of truth for the application. To update it, you would typically run a Python script that scans the Markdown files, validates their frontmatter, and compiles them into the JSON format. **Note:** The script for this is not yet in the repository and needs to be created.
3.  **Rebuild the Application:** Run `pnpm build` to ensure all changes are reflected.
4.  **Deploy:** Push the changes to your Git repository to trigger an automatic deployment, or manually upload the updated `dist/public` directory.

### 6.2. Regenerating Slugs & Relationships

If you make significant changes to titles or add new capsules, you may need to regenerate slugs and graph relationships. The scripts for these tasks are not yet integrated into a single workflow but can be run manually:

- **Slug Regeneration:** The logic is contained within the Python scripts used in the remediation phase.
- **Graph Regeneration:** The logic is also available in the remediation scripts.

A unified `pnpm content:build` command should be created to streamline this process.

---

## 7. Monitoring & Maintenance

### 7.1. Analytics

If you have configured Umami or another analytics provider, monitor user traffic and behavior through their dashboard. This can provide insights into popular content and user navigation patterns.

### 7.2. Dependency Updates

Regularly update dependencies to ensure the application remains secure and performant. Use `npm audit` or `pnpm audit` to check for vulnerabilities.

```bash
pnpm audit
```

### 7.3. Backups

- **Code:** The code is backed up via the Git repository.
- **Content:** The Markdown capsules should be stored in a separate version-controlled repository (`ApsnyTravelCatalog`).

---

**Generated by:** Manus AI
