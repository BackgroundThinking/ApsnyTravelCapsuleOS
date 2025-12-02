import { z } from "zod";

export interface SearchDocument {
  id: string;
  slug: string;
  title: string;
  type: "product" | "place" | "guide";
  description: string;
  keywords: string[];
  content: string;
  region: string;
  emoji: string;
}

export interface SearchResult {
  document: SearchDocument;
  score: number;
  highlights: string[];
}

/**
 * Simple client-side search implementation
 * For production, consider using Fuse.js for better fuzzy matching
 */
export class CapsuleSearch {
  private documents: SearchDocument[] = [];
  private index: Map<string, SearchDocument[]> = new Map();

  async loadIndex(): Promise<void> {
    try {
      const response = await fetch("/search-index.json");
      this.documents = await response.json();
      this.buildIndex();
    } catch (error) {
      console.error("Failed to load search index:", error);
    }
  }

  private buildIndex(): void {
    // Build keyword index for faster searching
    for (const doc of this.documents) {
      // Index by keywords
      for (const keyword of doc.keywords) {
        const key = keyword.toLowerCase();
        if (!this.index.has(key)) {
          this.index.set(key, []);
        }
        this.index.get(key)!.push(doc);
      }

      // Index by title words
      const titleWords = doc.title.toLowerCase().split(/\s+/);
      for (const word of titleWords) {
        if (word.length > 2) {
          if (!this.index.has(word)) {
            this.index.set(word, []);
          }
          if (!this.index.get(word)!.includes(doc)) {
            this.index.get(word)!.push(doc);
          }
        }
      }
    }
  }

  search(query: string, limit: number = 10): SearchResult[] {
    if (!query || query.length < 2) {
      return [];
    }

    const queryLower = query.toLowerCase();
    const results: Map<string, number> = new Map();

    // Search by keywords
    this.index.forEach((docs, keyword) => {
      if (keyword.includes(queryLower) || queryLower.includes(keyword)) {
        for (const doc of docs) {
          const score = results.get(doc.id) || 0;
          results.set(doc.id, score + 2);
        }
      }
    });

    // Search by title
    for (const doc of this.documents) {
      if (doc.title.toLowerCase().includes(queryLower)) {
        const score = results.get(doc.id) || 0;
        results.set(doc.id, score + 3);
      }
    }

    // Search by description
    for (const doc of this.documents) {
      if (doc.description.toLowerCase().includes(queryLower)) {
        const score = results.get(doc.id) || 0;
        results.set(doc.id, score + 1);
      }
    }

    // Convert to sorted results
    return Array.from(results.entries())
      .map(([id, score]) => ({
        document: this.documents.find(d => d.id === id)!,
        score,
        highlights: this.extractHighlights(
          this.documents.find(d => d.id === id)!,
          queryLower
        ),
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }

  private extractHighlights(doc: SearchDocument, query: string): string[] {
    const highlights: string[] = [];

    // Extract highlights from title
    if (doc.title.toLowerCase().includes(query)) {
      highlights.push(doc.title);
    }

    // Extract highlights from description
    if (doc.description.toLowerCase().includes(query)) {
      const start = Math.max(0, doc.description.toLowerCase().indexOf(query) - 30);
      const end = Math.min(doc.description.length, start + 100);
      highlights.push("..." + doc.description.substring(start, end) + "...");
    }

    return highlights.slice(0, 2);
  }

  getDocumentById(id: string): SearchDocument | undefined {
    return this.documents.find(d => d.id === id);
  }

  getDocumentsByType(type: "product" | "place" | "guide"): SearchDocument[] {
    return this.documents.filter(d => d.type === type);
  }

  getDocumentsByRegion(region: string): SearchDocument[] {
    return this.documents.filter(d => d.region === region);
  }
}

// Export singleton instance
export const capsuleSearch = new CapsuleSearch();
