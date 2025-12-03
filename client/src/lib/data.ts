import { z } from "zod";

/**
 * Zod schema for validating Capsule data structure
 * 
 * Defines the complete structure of a travel capsule including:
 * - Basic information (id, type, tier, slug, title, emoji)
 * - Temporal data (season, duration)
 * - Geographic data (coordinates and region)
 * - Relationship links (parent, children, siblings, related)
 * - SEO metadata (title, description, keywords)
 * - Content metadata (created, updated, version)
 * - Main content body
 */
export const CapsuleSchema = z.object({
  id: z.string(),
  type: z.string(),
  tier: z.number(),
  slug: z.string(),
  title: z.string(),
  emoji: z.string(),
  season: z.array(z.string()),
  duration: z.string(),
  geo: z.object({
    lat: z.number(),
    lng: z.number(),
    region: z.string(),
  }),
  links: z.object({
    parent: z.array(z.string()),
    children: z.array(z.string()),
    siblings: z.array(z.string()),
    related: z.array(z.string()),
  }),
  seo: z.object({
    title: z.string(),
    description: z.string(),
    keywords: z.array(z.string()),
  }),
  metadata: z.object({
    created: z.string(),
    updated: z.string(),
    version: z.string(),
  }),
  content: z.string(),
});

/**
 * TypeScript type inferred from CapsuleSchema
 * 
 * Represents a single travel capsule with all its associated data.
 * Use this type for type-safe capsule handling throughout the application.
 */
export type Capsule = z.infer<typeof CapsuleSchema>;

/**
 * Fetches all capsules from the capsules.json data file
 * 
 * This function retrieves the complete list of travel capsules from the static
 * JSON data file and validates each capsule against the CapsuleSchema.
 * 
 * @returns {Promise<Capsule[]>} A promise that resolves to an array of validated Capsule objects
 * @throws {Error} If the fetch request fails or the data doesn't match the schema
 * 
 * @example
 * ```typescript
 * const capsules = await fetchCapsules();
 * console.log(`Loaded ${capsules.length} capsules`);
 * ```
 */
export async function fetchCapsules(): Promise<Capsule[]> {
  const response = await fetch("/capsules.json");
  if (!response.ok) {
    throw new Error("Failed to fetch capsules");
  }
  const data = await response.json();
  return z.array(CapsuleSchema).parse(data.capsules);
}

/**
 * Fetches a single capsule by its unique slug identifier
 * 
 * Retrieves all capsules and filters to find the one matching the provided slug.
 * The slug is a URL-friendly identifier used for routing and SEO purposes.
 * 
 * @param {string} slug - The unique slug identifier for the capsule (e.g., "abkhazian-cuisine")
 * @returns {Promise<Capsule | undefined>} A promise that resolves to the matching Capsule or undefined if not found
 * @throws {Error} If the fetch request fails or the data doesn't match the schema
 * 
 * @example
 * ```typescript
 * const capsule = await fetchCapsuleBySlug("abkhazian-cuisine");
 * if (capsule) {
 *   console.log(`Found capsule: ${capsule.title}`);
 * } else {
 *   console.log("Capsule not found");
 * }
 * ```
 */
export async function fetchCapsuleBySlug(slug: string): Promise<Capsule | undefined> {
  const capsules = await fetchCapsules();
  return capsules.find((c) => c.slug === slug);
}

/**
 * Fetches all capsules that match a specific category
 * 
 * Filters capsules based on category, checking both the capsule type field
 * and the SEO keywords array. This allows for flexible categorization where
 * a capsule can be found through multiple category paths.
 * 
 * @param {string} category - The category to filter by (e.g., "place", "product", "experience")
 * @returns {Promise<Capsule[]>} A promise that resolves to an array of matching Capsule objects
 * @throws {Error} If the fetch request fails or the data doesn't match the schema
 * 
 * @example
 * ```typescript
 * const placeCapsules = await fetchCapsulesByCategory("place");
 * console.log(`Found ${placeCapsules.length} place capsules`);
 * ```
 * 
 * @remarks
 * The current implementation checks if the category matches either:
 * - The capsule's type field
 * - Any keyword in the capsule's SEO keywords array
 * 
 * This logic may need adjustment based on evolving data structure requirements.
 */
export async function fetchCapsulesByCategory(category: string): Promise<Capsule[]> {
  const capsules = await fetchCapsules();
  // Note: Category logic might need adjustment based on actual data structure
  // For now, we filter by type or check if category is in keywords
  return capsules.filter((c) => c.type === category || c.seo.keywords.includes(category));
}
