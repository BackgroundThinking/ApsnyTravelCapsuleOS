"""
Data Models for ApsnyTravel-CapsuleOS Integration Algorithm
Defines the canonical data structure for capsules using Pydantic
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class GeoModel(BaseModel):
    """Geospatial data for a capsule"""
    lat: float = Field(..., description="Latitude coordinate")
    lng: float = Field(..., description="Longitude coordinate")
    region: str = Field(..., description="Geographical region")

    class Config:
        json_schema_extra = {
            "example": {
                "lat": 43.4833,
                "lng": 40.5333,
                "region": "abkhazia"
            }
        }


class LinksModel(BaseModel):
    """Relationship links to other capsules"""
    parent: List[str] = Field(default_factory=list, description="Parent capsule IDs")
    children: List[str] = Field(default_factory=list, description="Child capsule IDs")
    related: List[str] = Field(default_factory=list, description="Related capsule IDs")
    siblings: List[str] = Field(default_factory=list, description="Sibling capsule IDs")

    class Config:
        json_schema_extra = {
            "example": {
                "parent": ["product-winter-tours"],
                "children": [],
                "related": ["place-lake-ritsa", "guide-winter-photography"],
                "siblings": []
            }
        }


class SEOModel(BaseModel):
    """SEO metadata for a capsule"""
    title: str = Field(..., description="SEO-optimized title")
    description: str = Field(..., description="Meta description for search engines")
    keywords: List[str] = Field(..., description="Relevant keywords")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Lake Ritsa Winter - Abkhazia's Most Beautiful Alpine Lake",
                "description": "Discover Lake Ritsa in winter: pristine alpine beauty, snow-covered peaks, and unforgettable mountain views.",
                "keywords": ["lake ritsa", "abkhazia", "winter", "alpine", "mountain"]
            }
        }


class MetadataModel(BaseModel):
    """Metadata about the capsule"""
    created: str = Field(..., description="Creation date in YYYY-MM-DD format")
    updated: str = Field(..., description="Last updated date in YYYY-MM-DD format")
    source: str = Field(default="apsnytravel.ru", description="Source of the content")
    version: str = Field(default="1.0", description="Content version")

    class Config:
        json_schema_extra = {
            "example": {
                "created": "2025-01-15",
                "updated": "2025-12-02",
                "source": "apsnytravel.ru",
                "version": "1.0"
            }
        }


class CapsuleModel(BaseModel):
    """Canonical data model for a single capsule"""
    id: str = Field(..., description="Unique identifier")
    type: str = Field(..., description="Type: product, place, or guide")
    tier: int = Field(..., description="Content hierarchy tier")
    slug: str = Field(..., description="URL-friendly slug")
    title: str = Field(..., description="Main title")
    emoji: str = Field(..., description="Representative emoji")
    geo: GeoModel = Field(..., description="Geospatial information")
    links: LinksModel = Field(default_factory=LinksModel, description="Relationship links")
    seo: SEOModel = Field(..., description="SEO metadata")
    content: str = Field(..., description="Full content (Markdown)")
    metadata: MetadataModel = Field(default_factory=MetadataModel, description="Content metadata")

    @validator('type')
    def validate_type(cls, v):
        if v not in ['product', 'place', 'guide']:
            raise ValueError('type must be one of: product, place, guide')
        return v

    @validator('tier')
    def validate_tier(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('tier must be 1, 2, or 3')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "place-lake-ritsa-winter",
                "type": "place",
                "tier": 2,
                "slug": "place/lake-ritsa-winter",
                "title": "Lake Ritsa (Winter)",
                "emoji": "🏔️",
                "geo": {
                    "lat": 43.4833,
                    "lng": 40.5333,
                    "region": "abkhazia"
                },
                "links": {
                    "parent": ["product-winter-tours"],
                    "children": [],
                    "related": ["guide-winter-photography"],
                    "siblings": []
                },
                "seo": {
                    "title": "Lake Ritsa Winter - Abkhazia's Most Beautiful Alpine Lake",
                    "description": "Discover Lake Ritsa in winter...",
                    "keywords": ["lake ritsa", "abkhazia", "winter"]
                },
                "content": "Lake Ritsa is...",
                "metadata": {
                    "created": "2025-01-15",
                    "updated": "2025-12-02",
                    "source": "apsnytravel.ru",
                    "version": "1.0"
                }
            }
        }


class CapsuleCollectionModel(BaseModel):
    """Collection of all capsules"""
    capsules: List[CapsuleModel] = Field(..., description="Array of capsules")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Collection metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "capsules": [],
                "metadata": {
                    "total": 53,
                    "generated": "2025-12-02T22:00:00Z",
                    "version": "0.0.1"
                }
            }
        }
