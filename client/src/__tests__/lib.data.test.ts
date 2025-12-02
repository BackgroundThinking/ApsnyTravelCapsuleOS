import { describe, it, expect, beforeAll } from "vitest";
import { fetchCapsules, fetchCapsuleBySlug, CapsuleSchema } from "@/lib/data";

describe("Data Layer - Capsule Fetching", () => {
  let capsules: any[] = [];

  beforeAll(async () => {
    capsules = await fetchCapsules();
  });

  it("should fetch all capsules", async () => {
    expect(capsules).toBeDefined();
    expect(capsules.length).toBeGreaterThan(0);
  });

  it("should have 53 capsules", async () => {
    expect(capsules.length).toBe(53);
  });

  it("should validate capsule schema", async () => {
    for (const capsule of capsules) {
      const result = CapsuleSchema.safeParse(capsule);
      expect(result.success).toBe(true);
    }
  });

  it("should have unique slugs", async () => {
    const slugs = capsules.map((c) => c.slug);
    const uniqueSlugs = new Set(slugs);
    expect(uniqueSlugs.size).toBe(slugs.length);
  });

  it("should have unique IDs", async () => {
    const ids = capsules.map((c) => c.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it("should find capsule by slug", async () => {
    const firstCapsule = capsules[0];
    const capsule = await fetchCapsuleBySlug(firstCapsule.slug);
    expect(capsule).toBeDefined();
    expect(capsule?.slug).toBe(firstCapsule.slug);
  });

  it("should return undefined for non-existent slug", async () => {
    const capsule = await fetchCapsuleBySlug("non/existent");
    expect(capsule).toBeUndefined();
  });

  it("should have complete SEO metadata", async () => {
    for (const capsule of capsules) {
      expect(capsule.seo.title).toBeDefined();
      expect(capsule.seo.description).toBeDefined();
      expect(capsule.seo.keywords).toBeDefined();
      expect(capsule.seo.keywords.length).toBeGreaterThan(0);
    }
  });

  it("should have valid geospatial data", async () => {
    for (const capsule of capsules) {
      expect(capsule.geo.lat).toBeDefined();
      expect(capsule.geo.lng).toBeDefined();
      expect(capsule.geo.region).toBeDefined();
      expect(typeof capsule.geo.lat).toBe("number");
      expect(typeof capsule.geo.lng).toBe("number");
    }
  });

  it("should have content for all capsules", async () => {
    for (const capsule of capsules) {
      expect(capsule.content).toBeDefined();
      expect(capsule.content.length).toBeGreaterThan(100);
    }
  });
});
