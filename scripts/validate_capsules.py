#!/usr/bin/env python3
"""
Capsule Validation Script

Validates capsule data integrity and completeness.

Usage:
    python3 validate_capsules.py [--strict] [--fix]
    
Examples:
    python3 validate_capsules.py              # Standard validation
    python3 validate_capsules.py --strict     # Strict validation
    python3 validate_capsules.py --fix        # Fix common issues
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse

class CapsuleValidator:
    """Validates capsule data."""
    
    REQUIRED_FIELDS = {
        "id", "type", "tier", "slug", "title", "emoji",
        "season", "duration", "geo", "links", "seo", "metadata", "content"
    }
    
    OPTIONAL_FIELDS = {
        "image_url", "gallery_images", "description", "highlights",
        "price", "rating", "practical_info", "accessibility", "category_tags"
    }
    
    def __init__(self, capsules_path: str = "client/public/capsules.json"):
        self.capsules_path = Path(capsules_path)
        self.data = None
        self.errors = []
        self.warnings = []
        self.load_capsules()
    
    def load_capsules(self) -> None:
        """Load capsules from JSON file."""
        if not self.capsules_path.exists():
            raise FileNotFoundError(f"Capsules file not found: {self.capsules_path}")
        
        try:
            with open(self.capsules_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in capsules file: {e}")
    
    def validate_structure(self) -> bool:
        """Validate overall structure."""
        if not isinstance(self.data, dict):
            self.errors.append("Root must be a dictionary")
            return False
        
        if "capsules" not in self.data:
            self.errors.append("Missing 'capsules' key in root")
            return False
        
        if not isinstance(self.data["capsules"], list):
            self.errors.append("'capsules' must be a list")
            return False
        
        return True
    
    def validate_capsule(self, capsule: Dict[str, Any], index: int) -> Tuple[bool, List[str]]:
        """Validate individual capsule."""
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in capsule:
                errors.append(f"Capsule {index}: Missing required field '{field}'")
        
        # Check field types
        if not isinstance(capsule.get("id"), str):
            errors.append(f"Capsule {index}: 'id' must be string")
        
        if not isinstance(capsule.get("type"), str):
            errors.append(f"Capsule {index}: 'type' must be string")
        
        if not isinstance(capsule.get("tier"), int):
            errors.append(f"Capsule {index}: 'tier' must be integer")
        
        # Check geo data
        geo = capsule.get("geo", {})
        if not isinstance(geo, dict):
            errors.append(f"Capsule {index}: 'geo' must be dictionary")
        else:
            if "lat" not in geo or "lng" not in geo:
                errors.append(f"Capsule {index}: 'geo' missing lat/lng")
        
        # Check links structure
        links = capsule.get("links", {})
        if not isinstance(links, dict):
            errors.append(f"Capsule {index}: 'links' must be dictionary")
        else:
            required_link_fields = {"parent", "children", "siblings", "related"}
            for field in required_link_fields:
                if field not in links:
                    errors.append(f"Capsule {index}: 'links' missing '{field}'")
        
        # Check SEO data
        seo = capsule.get("seo", {})
        if not isinstance(seo, dict):
            errors.append(f"Capsule {index}: 'seo' must be dictionary")
        else:
            if "title" not in seo or "description" not in seo or "keywords" not in seo:
                errors.append(f"Capsule {index}: 'seo' incomplete")
        
        # Check metadata
        metadata = capsule.get("metadata", {})
        if not isinstance(metadata, dict):
            errors.append(f"Capsule {index}: 'metadata' must be dictionary")
        else:
            if "created" not in metadata or "updated" not in metadata or "version" not in metadata:
                errors.append(f"Capsule {index}: 'metadata' incomplete")
        
        # Optional field type checks
        if "gallery_images" in capsule:
            if not isinstance(capsule["gallery_images"], list):
                errors.append(f"Capsule {index}: 'gallery_images' must be list")
        
        if "highlights" in capsule:
            if not isinstance(capsule["highlights"], list):
                errors.append(f"Capsule {index}: 'highlights' must be list")
        
        if "rating" in capsule:
            if not isinstance(capsule["rating"], (int, float)):
                errors.append(f"Capsule {index}: 'rating' must be number")
            elif not (4.0 <= capsule["rating"] <= 5.0):
                errors.append(f"Capsule {index}: 'rating' must be between 4.0 and 5.0")
        
        return len(errors) == 0, errors
    
    def validate_all(self, strict: bool = False) -> bool:
        """Validate all capsules."""
        if not self.validate_structure():
            return False
        
        capsules = self.data.get("capsules", [])
        valid_count = 0
        
        for i, capsule in enumerate(capsules):
            is_valid, errors = self.validate_capsule(capsule, i)
            
            if is_valid:
                valid_count += 1
            else:
                self.errors.extend(errors)
        
        print(f"✓ Validated {valid_count}/{len(capsules)} capsules")
        
        return len(self.errors) == 0
    
    def print_report(self) -> None:
        """Print validation report."""
        print("\n" + "=" * 80)
        print("CAPSULE VALIDATION REPORT")
        print("=" * 80)
        
        capsules = self.data.get("capsules", [])
        
        # Summary statistics
        print(f"\nTotal Capsules: {len(capsules)}")
        
        by_type = {}
        by_tier = {}
        for c in capsules:
            type_name = c.get("type", "unknown")
            tier = c.get("tier", "unknown")
            by_type[type_name] = by_type.get(type_name, 0) + 1
            by_tier[tier] = by_tier.get(tier, 0) + 1
        
        print(f"\nBy Type:")
        for type_name, count in sorted(by_type.items()):
            print(f"  - {type_name}: {count}")
        
        print(f"\nBy Tier:")
        for tier, count in sorted(by_tier.items()):
            print(f"  - Tier {tier}: {count}")
        
        # Data completeness
        print(f"\nData Completeness:")
        fields_check = {}
        for field in self.OPTIONAL_FIELDS:
            count = sum(1 for c in capsules if field in c and c[field])
            coverage = (count / len(capsules)) * 100 if capsules else 0
            status = "✓" if coverage == 100 else "⚠" if coverage > 50 else "✗"
            fields_check[field] = (count, coverage, status)
            print(f"  {status} {field}: {count}/{len(capsules)} ({coverage:.1f}%)")
        
        # Errors and warnings
        if self.errors:
            print(f"\n✗ ERRORS ({len(self.errors)}):")
            for error in self.errors[:10]:
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")
        else:
            print(f"\n✓ No errors found")
        
        if self.warnings:
            print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")
        
        print("\n" + "=" * 80)
        
        if self.errors:
            print("✗ VALIDATION FAILED")
            return False
        else:
            print("✓ VALIDATION PASSED")
            return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate capsule data integrity"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict validation"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix common issues"
    )
    
    args = parser.parse_args()
    
    try:
        validator = CapsuleValidator()
        is_valid = validator.validate_all(strict=args.strict)
        validator.print_report()
        
        return 0 if is_valid else 1
    
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
