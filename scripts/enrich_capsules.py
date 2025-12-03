#!/usr/bin/env python3
"""
Capsule Enrichment Script

This script enriches all Tier-2 capsules (places and guides) with:
- Gallery images
- Descriptions
- Highlights
- Ratings
- Practical information
- Accessibility data

Usage:
    python3 enrich_capsules.py [--places] [--guides] [--all]
    
Examples:
    python3 enrich_capsules.py --all          # Enrich all capsules
    python3 enrich_capsules.py --places       # Enrich only places
    python3 enrich_capsules.py --guides       # Enrich only guides
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import argparse
from datetime import datetime

class CapsuleEnricher:
    """Enriches capsules with additional data."""
    
    def __init__(self, capsules_path: str = "client/public/capsules.json"):
        self.capsules_path = Path(capsules_path)
        self.data = None
        self.backup_path = None
        self.load_capsules()
    
    def load_capsules(self) -> None:
        """Load capsules from JSON file."""
        if not self.capsules_path.exists():
            raise FileNotFoundError(f"Capsules file not found: {self.capsules_path}")
        
        with open(self.capsules_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        print(f"✓ Loaded {len(self.data.get('capsules', []))} capsules")
    
    def backup_capsules(self) -> None:
        """Create backup of original capsules."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = self.capsules_path.parent / f"capsules_backup_{timestamp}.json"
        
        with open(self.backup_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Backup created: {self.backup_path}")
    
    def save_capsules(self) -> None:
        """Save enriched capsules to JSON file."""
        with open(self.capsules_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved enriched capsules to {self.capsules_path}")
    
    def enrich_places(self, enrichment_data: Dict[str, Any]) -> int:
        """Enrich place capsules."""
        count = 0
        capsules = self.data.get("capsules", [])
        
        for capsule in capsules:
            if capsule.get("type") != "place" or capsule.get("tier") != 2:
                continue
            
            capsule_id = capsule.get("id")
            if capsule_id not in enrichment_data:
                continue
            
            data = enrichment_data[capsule_id]
            
            # Add gallery images
            if "gallery_images" in data:
                capsule["gallery_images"] = data["gallery_images"]
            
            # Add description
            if "description" in data:
                capsule["description"] = data["description"]
            
            # Add highlights
            if "highlights" in data:
                capsule["highlights"] = data["highlights"]
            
            # Add rating
            if "rating" in data:
                capsule["rating"] = data["rating"]
            
            # Add practical info
            if "practical_info" in data:
                capsule["practical_info"] = data["practical_info"]
            
            # Add accessibility
            if "accessibility" in data:
                capsule["accessibility"] = data["accessibility"]
            
            # Update metadata
            capsule["metadata"]["updated"] = datetime.now().strftime("%Y-%m-%d")
            capsule["metadata"]["version"] = "2.0.0"
            
            count += 1
        
        print(f"✓ Enriched {count} place capsules")
        return count
    
    def enrich_guides(self, enrichment_data: Dict[str, Any]) -> int:
        """Enrich guide capsules."""
        count = 0
        capsules = self.data.get("capsules", [])
        
        for capsule in capsules:
            if capsule.get("type") != "guide" or capsule.get("tier") != 2:
                continue
            
            capsule_id = capsule.get("id")
            if capsule_id not in enrichment_data:
                continue
            
            data = enrichment_data[capsule_id]
            
            # Add gallery images
            if "gallery_images" in data:
                capsule["gallery_images"] = data["gallery_images"]
            
            # Add description
            if "description" in data:
                capsule["description"] = data["description"]
            
            # Add highlights (key takeaways for guides)
            if "highlights" in data:
                capsule["highlights"] = data["highlights"]
            
            # Add rating
            if "rating" in data:
                capsule["rating"] = data["rating"]
            
            # Update metadata
            capsule["metadata"]["updated"] = datetime.now().strftime("%Y-%m-%d")
            capsule["metadata"]["version"] = "2.0.0"
            
            count += 1
        
        print(f"✓ Enriched {count} guide capsules")
        return count
    
    def validate_enrichment(self) -> Dict[str, Any]:
        """Validate enrichment completeness."""
        stats = {
            "total": 0,
            "with_gallery": 0,
            "with_description": 0,
            "with_highlights": 0,
            "with_rating": 0,
            "fully_enriched": 0
        }
        
        for capsule in self.data.get("capsules", []):
            if capsule.get("tier") != 2:
                continue
            
            stats["total"] += 1
            
            if capsule.get("gallery_images"):
                stats["with_gallery"] += 1
            
            if capsule.get("description"):
                stats["with_description"] += 1
            
            if capsule.get("highlights"):
                stats["with_highlights"] += 1
            
            if capsule.get("rating"):
                stats["with_rating"] += 1
            
            if all([
                capsule.get("gallery_images"),
                capsule.get("description"),
                capsule.get("highlights"),
                capsule.get("rating")
            ]):
                stats["fully_enriched"] += 1
        
        return stats
    
    def print_validation_report(self, stats: Dict[str, Any]) -> None:
        """Print validation report."""
        print("\n" + "=" * 80)
        print("ENRICHMENT VALIDATION REPORT")
        print("=" * 80)
        
        total = stats["total"]
        print(f"\nTotal Tier-2 Capsules: {total}")
        print(f"  ✓ With Gallery Images: {stats['with_gallery']}/{total} ({stats['with_gallery']/total*100:.1f}%)")
        print(f"  ✓ With Description: {stats['with_description']}/{total} ({stats['with_description']/total*100:.1f}%)")
        print(f"  ✓ With Highlights: {stats['with_highlights']}/{total} ({stats['with_highlights']/total*100:.1f}%)")
        print(f"  ✓ With Rating: {stats['with_rating']}/{total} ({stats['with_rating']/total*100:.1f}%)")
        print(f"  ✓ Fully Enriched: {stats['fully_enriched']}/{total} ({stats['fully_enriched']/total*100:.1f}%)")
        
        print("\n" + "=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Enrich capsules with additional data"
    )
    parser.add_argument(
        "--places",
        action="store_true",
        help="Enrich only place capsules"
    )
    parser.add_argument(
        "--guides",
        action="store_true",
        help="Enrich only guide capsules"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Enrich all capsules (default)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate current enrichment status"
    )
    
    args = parser.parse_args()
    
    try:
        enricher = CapsuleEnricher()
        
        if args.validate_only:
            stats = enricher.validate_enrichment()
            enricher.print_validation_report(stats)
            return 0
        
        # Create backup
        enricher.backup_capsules()
        
        # Load enrichment data
        enrichment_data = {}
        
        # For now, this script provides the framework
        # Actual enrichment data should be loaded from:
        # - data/enrichment_data/place_descriptions.json
        # - data/enrichment_data/place_highlights.json
        # - data/enrichment_data/guide_descriptions.json
        # - data/enrichment_data/guide_highlights.json
        
        print("\n⚠ Note: Enrichment data files not found.")
        print("Please generate enrichment data using:")
        print("  - scripts/generate_descriptions.py")
        print("  - scripts/generate_highlights.py")
        print("  - scripts/assign_ratings.py")
        
        # Determine what to enrich
        should_enrich_places = args.places or args.all or (not args.guides and not args.all)
        should_enrich_guides = args.guides or args.all or (not args.places and not args.all)
        
        if should_enrich_places:
            enricher.enrich_places(enrichment_data)
        
        if should_enrich_guides:
            enricher.enrich_guides(enrichment_data)
        
        # Save enriched capsules
        enricher.save_capsules()
        
        # Validate
        stats = enricher.validate_enrichment()
        enricher.print_validation_report(stats)
        
        return 0
    
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
