import { describe, it, expect, beforeAll } from "vitest";
import { capsuleSearch } from "@/lib/search";

describe("Search Module", () => {
  beforeAll(async () => {
    await capsuleSearch.loadIndex();
  });

  it("should load search index", async () => {
    const results = capsuleSearch.search("lake");
    expect(results).toBeDefined();
  });

  it("should search by title", async () => {
    const results = capsuleSearch.search("lake");
    expect(results.length).toBeGreaterThan(0);
  });

  it("should search by keywords", async () => {
    const results = capsuleSearch.search("abkhazia");
    expect(results.length).toBeGreaterThan(0);
  });

  it("should return empty for short queries", async () => {
    const results = capsuleSearch.search("a");
    expect(results.length).toBe(0);
  });

  it("should filter by type", async () => {
    const places = capsuleSearch.getDocumentsByType("place");
    expect(places.length).toBeGreaterThan(0);
    expect(places.every((p) => p.type === "place")).toBe(true);
  });

  it("should filter by region", async () => {
    const abkhazian = capsuleSearch.getDocumentsByRegion("abkhazia");
    expect(abkhazian.length).toBeGreaterThan(0);
  });

  it("should sort results by relevance", async () => {
    const results = capsuleSearch.search("lake");
    if (results.length > 1) {
      expect(results[0].score).toBeGreaterThanOrEqual(results[1].score);
    }
  });
});
