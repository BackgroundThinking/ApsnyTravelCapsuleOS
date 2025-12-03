import { z } from "zod";

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

export type Capsule = z.infer<typeof CapsuleSchema>;

export async function fetchCapsules(): Promise<Capsule[]> {
  const response = await fetch("/capsules.json");
  if (!response.ok) {
    throw new Error("Failed to fetch capsules");
  }
  const data = await response.json();
  return z.array(CapsuleSchema).parse(data.capsules);
}

export async function fetchCapsuleBySlug(
  slug: string
): Promise<Capsule | undefined> {
  const capsules = await fetchCapsules();
  return capsules.find(c => c.slug === slug);
}

export async function fetchCapsulesByCategory(
  category: string
): Promise<Capsule[]> {
  const capsules = await fetchCapsules();
  // Note: Category logic might need adjustment based on actual data structure
  // For now, we filter by type or check if category is in keywords
  return capsules.filter(
    c => c.type === category || c.seo.keywords.includes(category)
  );
}
