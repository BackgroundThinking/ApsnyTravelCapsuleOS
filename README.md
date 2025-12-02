# ApsnyTravel - Winter Tourism Platform 🏔️

> A modern, high-performance static web application for exploring winter tourism in Abkhazia and Sochi. Built with **CapsuleOS** architecture.

![ApsnyTravel Hero](/client/public/images/hero-winter-ritsa.jpg)

## 📋 Overview

**ApsnyTravel** is a curated digital guide designed to showcase the unique winter experiences of the Caucasus region—from the frozen beauty of Lake Ritsa to the steaming thermal springs of Kyndyg.

The platform is built on the **CapsuleOS** philosophy: content is organized into atomic "capsules" (Markdown files) that are compiled into a static JSON API at build time. This ensures blazing fast performance, excellent SEO, and easy content management without a complex CMS.

### Key Features

-   **🇨🇭 Swiss Style Design**: A clean, objective, and typographic-centric interface inspired by Alpine Modernism.
-   **⚡ Static Performance**: Zero-latency navigation and instant page loads powered by Next.js (Static Export) or Vite.
-   **💎 Capsule Architecture**: Content is decoupled from code, stored as structured Markdown with frontmatter metadata.
-   **📱 Fully Responsive**: Optimized for all devices, from desktop monitors to mobile phones on the go.
-   **🔍 Rich Metadata**: Comprehensive cross-linking between Tours, Places, and Guides.

---

## 🛠️ Tech Stack

-   **Framework**: React 19 + Vite (Static Generation)
-   **Styling**: Tailwind CSS 4 + Shadcn UI
-   **Routing**: Wouter (Client-side routing)
-   **Data Layer**: Custom Python scripts for Markdown -> JSON compilation
-   **Typography**: Unbounded (Headings) + Inter (Body)
-   **Icons**: Lucide React

---

## 🚀 Getting Started

### Prerequisites

-   Node.js 18+
-   Python 3.11+ (for content generation)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/num1hub/apsnytravel-web.git
    cd apsnytravel-web
    ```

2.  **Install dependencies:**
    ```bash
    pnpm install
    ```

3.  **Generate Content Data:**
    This step compiles the Markdown capsules into `client/public/capsules.json`.
    ```bash
    python3 ../generate_capsules_metadata.py
    ```

4.  **Start Development Server:**
    ```bash
    pnpm dev
    ```
    The site will be available at `http://localhost:3000`.

---

## 📂 Project Structure

```
apsnytravel-web/
├── client/
│   ├── public/             # Static assets (images, capsules.json)
│   ├── src/
│   │   ├── components/     # React components (Navigation, Footer, UI)
│   │   ├── pages/          # Page views (Home, Tours, Places)
│   │   ├── lib/            # Utilities (Data fetching, Zod schemas)
│   │   └── index.css       # Global styles & Design Tokens
├── server/                 # (Unused in static mode)
├── generate_capsules_metadata.py # Content compilation script
└── README.md               # This file
```

---

## 🎨 Design System

The project follows a strict **"Alpine Modernism"** design language:

-   **Primary Color**: International Orange (`#FF4F00`) - Used for CTAs and accents.
-   **Background**: Stark White (`#FFFFFF`) - For maximum readability.
-   **Typography**:
    -   **Headings**: `Unbounded` - Bold, extended, technical.
    -   **Body**: `Inter` - Clean, neutral, legible.
-   **Layout**: Asymmetric grids, high contrast, functional whitespace.

---

## 📝 Content Management

Content is managed in the `ApsnyTravelCatalog` repository (or local `capsules/` directory).

To add a new place:
1.  Create a new `.md` file in `capsules/tier2-deeplinks/places/`.
2.  Follow the standard frontmatter schema (Slug, Category, Related Tours).
3.  Run the generation script to update the app data.

*See `CONTENT_GUIDE.md` for detailed instructions.*

---

## 📄 License

MIT License. See `LICENSE` for details.

---

*Built with ❤️ by Manus AI for ApsnyTravel.*
