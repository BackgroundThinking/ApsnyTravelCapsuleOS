/**
 * SEO Utilities
 * Provides functions for generating and managing SEO meta tags
 */

import { Capsule } from "./data";

export interface SEOMetaTags {
  title: string;
  description: string;
  keywords: string;
  ogTitle: string;
  ogDescription: string;
  ogImage: string;
  ogUrl: string;
  twitterCard: string;
  twitterTitle: string;
  twitterDescription: string;
  twitterImage: string;
  canonical: string;
}

/**
 * Generate SEO meta tags for a capsule
 */
export function generateCapsuleSEOTags(
  capsule: Capsule,
  baseUrl: string = "https://apsnytravel.com"
): SEOMetaTags {
  const url = `${baseUrl}/capsule/${capsule.slug}`;
  const image = `${baseUrl}/images/og-${capsule.type}.jpg`;

  return {
    title: capsule.seo.title,
    description: capsule.seo.description,
    keywords: capsule.seo.keywords.join(", "),
    ogTitle: capsule.seo.title,
    ogDescription: capsule.seo.description,
    ogImage: image,
    ogUrl: url,
    twitterCard: "summary_large_image",
    twitterTitle: capsule.seo.title,
    twitterDescription: capsule.seo.description,
    twitterImage: image,
    canonical: url,
  };
}

/**
 * Generate SEO meta tags for the home page
 */
export function generateHomeSEOTags(
  baseUrl: string = "https://apsnytravel.com"
): SEOMetaTags {
  return {
    title: "ApsnyTravel - Winter Tourism Guide for Abkhazia & Sochi",
    description:
      "Discover the best winter destinations in Abkhazia and Sochi. Expert guides, travel tips, and local insights for an unforgettable experience.",
    keywords: "abkhazia, sochi, winter travel, tourism, guides, places",
    ogTitle: "ApsnyTravel - Winter Tourism Guide",
    ogDescription:
      "Discover the best winter destinations in Abkhazia and Sochi",
    ogImage: `${baseUrl}/images/og-home.jpg`,
    ogUrl: baseUrl,
    twitterCard: "summary_large_image",
    twitterTitle: "ApsnyTravel - Winter Tourism Guide",
    twitterDescription:
      "Discover the best winter destinations in Abkhazia and Sochi",
    twitterImage: `${baseUrl}/images/og-home.jpg`,
    canonical: baseUrl,
  };
}

/**
 * Inject SEO meta tags into the document head
 */
export function injectSEOMetaTags(tags: SEOMetaTags): void {
  // Remove existing meta tags
  const existingMetas = document.querySelectorAll('meta[data-seo="true"]');
  existingMetas.forEach(meta => meta.remove());

  const head = document.head;

  // Title
  document.title = tags.title;

  // Meta tags
  const metaTags = [
    { name: "description", content: tags.description },
    { name: "keywords", content: tags.keywords },
    { property: "og:title", content: tags.ogTitle },
    { property: "og:description", content: tags.ogDescription },
    { property: "og:image", content: tags.ogImage },
    { property: "og:url", content: tags.ogUrl },
    { property: "og:type", content: "website" },
    { name: "twitter:card", content: tags.twitterCard },
    { name: "twitter:title", content: tags.twitterTitle },
    { name: "twitter:description", content: tags.twitterDescription },
    { name: "twitter:image", content: tags.twitterImage },
  ];

  metaTags.forEach(({ name, property, content }) => {
    const meta = document.createElement("meta");
    if (name) meta.setAttribute("name", name);
    if (property) meta.setAttribute("property", property);
    meta.setAttribute("content", content);
    meta.setAttribute("data-seo", "true");
    head.appendChild(meta);
  });

  // Canonical link
  let canonical = document.querySelector('link[rel="canonical"]');
  if (!canonical) {
    canonical = document.createElement("link");
    canonical.setAttribute("rel", "canonical");
    head.appendChild(canonical);
  }
  canonical.setAttribute("href", tags.canonical);
}

/**
 * Generate Open Graph image URL for a capsule
 */
export function generateOGImageUrl(
  capsule: Capsule,
  baseUrl: string = "https://apsnytravel.com"
): string {
  // This would typically generate a dynamic OG image using a service like Vercel OG or similar
  // For now, return a placeholder
  return `${baseUrl}/images/og-${capsule.type}.jpg`;
}

/**
 * Generate structured breadcrumb data
 */
export function generateBreadcrumbs(
  capsule: Capsule,
  baseUrl: string = "https://apsnytravel.com"
): Array<{ name: string; url: string }> {
  const breadcrumbs: Array<{ name: string; url: string }> = [
    { name: "Home", url: baseUrl },
  ];

  // Add type-based breadcrumb
  const typeLabel =
    capsule.type.charAt(0).toUpperCase() + capsule.type.slice(1) + "s";
  breadcrumbs.push({
    name: typeLabel,
    url: `${baseUrl}/${capsule.type}s`,
  });

  // Add current page
  breadcrumbs.push({
    name: capsule.title,
    url: `${baseUrl}/capsule/${capsule.slug}`,
  });

  return breadcrumbs;
}
