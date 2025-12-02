import { Capsule } from "./data";

/**
 * Generate JSON-LD structured data for a capsule
 * This helps search engines understand the content better
 */
export function generateCapsuleSchema(capsule: Capsule): object {
  const schemaType = capsule.type === "product" ? "Product" : capsule.type === "place" ? "Place" : "Article";

  const schema: any = {
    "@context": "https://schema.org",
    "@type": schemaType,
    name: capsule.title,
    description: capsule.seo.description,
    url: `https://apsnytravel.com/capsule/${capsule.slug}`,
    keywords: capsule.seo.keywords.join(", "),
  };

  // Add geolocation
  if (capsule.geo) {
    schema.geo = {
      "@type": "GeoCoordinates",
      latitude: capsule.geo.lat,
      longitude: capsule.geo.lng,
    };

    schema.address = {
      "@type": "PostalAddress",
      addressRegion: capsule.geo.region,
      addressCountry: "RU",
    };
  }

  // Add metadata
  if (capsule.metadata) {
    schema.datePublished = capsule.metadata.created;
    schema.dateModified = capsule.metadata.updated;
  }

  return schema;
}

/**
 * Inject JSON-LD script into the page
 */
export function injectJsonLd(schema: object): void {
  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(schema);
  document.head.appendChild(script);
}

/**
 * Generate Organization schema for the site
 */
export function generateOrganizationSchema(): object {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "ApsnyTravel",
    url: "https://apsnytravel.com",
    logo: "https://apsnytravel.com/logo.png",
    description: "Winter tourism guide for Abkhazia and Sochi",
    sameAs: [
      "https://www.instagram.com/apsnytravel",
      "https://www.facebook.com/apsnytravel",
    ],
    contactPoint: {
      "@type": "ContactPoint",
      contactType: "Customer Support",
      email: "info@apsnytravel.com",
    },
  };
}

/**
 * Generate BreadcrumbList schema for navigation
 */
export function generateBreadcrumbSchema(items: { name: string; url: string }[]): object {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}
