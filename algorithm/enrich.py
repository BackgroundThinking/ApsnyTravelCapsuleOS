"""
Content Enrichment Module
Programmatically enhances capsule data with SEO metadata, structured data, and other attributes
"""

import logging
import re
from typing import Dict, Any, List
from models import CapsuleModel, SEOModel
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentEnricher:
    """Enriches capsule content with additional metadata and attributes"""

    # Common keywords for different types
    TYPE_KEYWORDS = {
        'product': ['tour', 'package', 'experience', 'adventure', 'travel'],
        'place': ['destination', 'location', 'site', 'attraction', 'landmark'],
        'guide': ['guide', 'tips', 'advice', 'information', 'tutorial']
    }

    @staticmethod
    def generate_slug(title: str, capsule_type: str = 'place') -> str:
        """
        Generate a URL-friendly slug from a title

        Args:
            title: The capsule title
            capsule_type: The capsule type (product, place, guide)

        Returns:
            A URL-friendly slug in format: type/slug-name
        """
        # Convert to lowercase
        slug = title.lower()

        # Replace spaces and special characters with hyphens
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)

        # Remove leading/trailing hyphens
        slug = slug.strip('-')

        # Limit length
        slug = slug[:50]

        return f"{capsule_type}/{slug}"

    @staticmethod
    def extract_keywords(title: str, content: str, capsule_type: str) -> List[str]:
        """
        Extract relevant keywords from title and content

        Args:
            title: The capsule title
            content: The capsule content
            capsule_type: The capsule type

        Returns:
            A list of relevant keywords
        """
        keywords = set()

        # Add type-specific keywords
        keywords.update(ContentEnricher.TYPE_KEYWORDS.get(capsule_type, []))

        # Add title words (longer than 3 characters)
        title_words = [w.lower() for w in title.split() if len(w) > 3]
        keywords.update(title_words)

        # Extract common words from content (very basic approach)
        # In production, use NLTK or similar for better extraction
        words = re.findall(r'\b\w{4,}\b', content.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Add most frequent words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        keywords.update([w[0] for w in top_words])

        return list(keywords)[:10]  # Limit to 10 keywords

    @staticmethod
    def generate_seo_description(title: str, content: str, max_length: int = 160) -> str:
        """
        Generate a SEO-optimized meta description

        Args:
            title: The capsule title
            content: The capsule content
            max_length: Maximum description length

        Returns:
            A SEO-optimized description
        """
        # Get first 2-3 sentences from content
        sentences = re.split(r'[.!?]+', content)
        description = '. '.join([s.strip() for s in sentences[:2] if s.strip()])

        # Ensure it includes the title
        if title.lower() not in description.lower():
            description = f"{title}. {description}"

        # Truncate to max length
        if len(description) > max_length:
            description = description[:max_length - 3] + '...'

        return description

    @staticmethod
    def generate_seo_title(title: str, region: str = '', capsule_type: str = 'place') -> str:
        """
        Generate a SEO-optimized title

        Args:
            title: The original title
            region: The geographical region
            capsule_type: The capsule type

        Returns:
            A SEO-optimized title
        """
        # Add region if provided
        if region and region.lower() not in title.lower():
            seo_title = f"{title} - {region.title()}"
        else:
            seo_title = title

        # Add type-specific suffix
        type_suffixes = {
            'product': 'Tour & Travel Package',
            'place': 'Travel Destination Guide',
            'guide': 'Travel Tips & Guide'
        }

        suffix = type_suffixes.get(capsule_type, 'Travel Guide')
        if suffix.lower() not in seo_title.lower():
            seo_title = f"{seo_title} | {suffix}"

        # Limit to 60 characters for optimal SEO
        if len(seo_title) > 60:
            seo_title = seo_title[:57] + '...'

        return seo_title

    @staticmethod
    def enrich_capsule(capsule: CapsuleModel) -> CapsuleModel:
        """
        Enrich a capsule with additional metadata

        Args:
            capsule: The capsule to enrich

        Returns:
            The enriched capsule
        """
        try:
            # Generate slug if not present or invalid
            if not capsule.slug or capsule.slug == '**':
                capsule.slug = ContentEnricher.generate_slug(capsule.title, capsule.type)

            # Extract keywords if missing
            if not capsule.seo.keywords or len(capsule.seo.keywords) == 0:
                capsule.seo.keywords = ContentEnricher.extract_keywords(
                    capsule.title,
                    capsule.content,
                    capsule.type
                )

            # Generate SEO title if missing or generic
            if not capsule.seo.title or len(capsule.seo.title) < 10:
                capsule.seo.title = ContentEnricher.generate_seo_title(
                    capsule.title,
                    capsule.geo.region,
                    capsule.type
                )

            # Generate SEO description if missing
            if not capsule.seo.description or len(capsule.seo.description) < 20:
                capsule.seo.description = ContentEnricher.generate_seo_description(
                    capsule.title,
                    capsule.content
                )

            # Update metadata timestamp
            capsule.metadata.updated = datetime.now().strftime('%Y-%m-%d')

            logger.debug(f"Enriched capsule: {capsule.id}")
            return capsule

        except Exception as e:
            logger.error(f"Error enriching capsule {capsule.id}: {str(e)}")
            return capsule

    @staticmethod
    def enrich_collection(capsules: List[CapsuleModel]) -> List[CapsuleModel]:
        """
        Enrich a collection of capsules

        Args:
            capsules: List of capsules to enrich

        Returns:
            List of enriched capsules
        """
        enriched = []
        for capsule in capsules:
            enriched.append(ContentEnricher.enrich_capsule(capsule))

        logger.info(f"Enriched {len(enriched)} capsules")
        return enriched
