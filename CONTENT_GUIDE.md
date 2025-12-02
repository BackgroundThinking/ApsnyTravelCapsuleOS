# Content Contribution Guide ✍️

Welcome to the ApsnyTravel content team! This guide explains how to create and edit "Capsules"—the building blocks of our platform.

---

## 📦 What is a Capsule?

A capsule is a single Markdown file that describes a specific entity: a **Tour**, a **Place**, or a **Guide**.

### File Location

-   **Tours**: `capsules/tier1-products/tour/`
-   **Places**: `capsules/tier2-deeplinks/places/{category}/`
-   **Guides**: `capsules/tier2-deeplinks/guides/`

---

## 📝 Creating a New Capsule

1.  **Create the File**: Name it using kebab-case (e.g., `my-new-place.md`).
2.  **Add Header**: Every file MUST start with a Level 1 Heading (`#`) containing an emoji and the title.
3.  **Add Metadata**: Immediately follow the title with the required metadata block.

### Template

```markdown
# 📍 Name of the Place

Slug: `place/name-of-place`
Category: `nature` (or culture, gastro, olympic)
Related Tours: #1, #4

> A brief, catchy summary of the place (1-2 sentences). This appears on cards.

---

## 📍 Information

| Parameter | Value |
|---|---|
| **Location** | City or Region |
| **Best Time** | Season or Time of Day |
| **Duration** | Recommended visit time |
| **Cost** | Price or "Free" |
| **Coordinates** | 00.0000, 00.0000 |

---

## 💎 Unique Features

-   **Feature 1**: Description...
-   **Feature 2**: Description...

---

## 📸 Photo Tips

-   **Best Spot**: Where to stand...
-   **Lighting**: When to shoot...

---

## 🔗 Related Capsules

**Tours:**
- [Tour Name](../../../tier1-products/tour/tour-file.md)

**Nearby:**
- [Place Name](../category/place-file.md)
```

---

## ⚠️ Rules & Best Practices

1.  **Slugs**: Must be unique. Format: `type/name` (e.g., `place/blue-lake`).
2.  **Images**: Do not embed images directly in Markdown yet. We handle images via the frontend assets folder.
3.  **Links**: Use relative paths for links.
    -   ✅ `../nature/lake.md`
    -   ❌ `/capsules/lake.md`
4.  **Tone**: Professional, inspiring, but factual. Avoid excessive exclamation marks.
5.  **Verification**: If you are unsure about a fact (like coordinates), add `[RESEARCH_NEEDED]` next to it.

---

## 🔍 Validation

Before committing, run the validation script to check for broken links or missing fields:

```bash
npm run validate
```

(Note: This script is located in the `ApsnyTravelCatalog` directory).
