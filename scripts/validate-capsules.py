#!/usr/bin/env python3
"""
Capsule Validation Script
Validates all capsules in capsules.json for data integrity and consistency
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

def validate_capsules(capsules_file: str = 'client/public/capsules.json') -> Tuple[bool, List[str]]:
    """Validate all capsules for integrity and consistency"""
    
    issues = []
    
    try:
        with open(capsules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        capsules = data['capsules']
    except FileNotFoundError:
        return False, [f"Capsules file not found: {capsules_file}"]
    except json.JSONDecodeError:
        return False, [f"Invalid JSON in {capsules_file}"]
    
    print(f"Validating {len(capsules)} capsules...\n")
    
    # Check required fields
    required_fields = ['id', 'type', 'tier', 'slug', 'title', 'emoji', 'geo', 'links', 'seo', 'content']
    for i, capsule in enumerate(capsules):
        for field in required_fields:
            if field not in capsule:
                issues.append(f"Capsule {i} ({capsule.get('id', 'UNKNOWN')}): Missing field '{field}'")
    
    # Check uniqueness
    ids = [c['id'] for c in capsules]
    slugs = [c['slug'] for c in capsules]
    
    for cid in ids:
        if ids.count(cid) > 1:
            issues.append(f"Duplicate ID: {cid}")
    
    for slug in slugs:
        if slugs.count(slug) > 1:
            issues.append(f"Duplicate slug: {slug}")
    
    # Check geospatial data
    for capsule in capsules:
        geo = capsule.get('geo', {})
        if not isinstance(geo.get('lat'), (int, float)) or not isinstance(geo.get('lng'), (int, float)):
            issues.append(f"Capsule '{capsule['id']}': Invalid coordinates")
    
    # Check graph relationships
    id_set = set(ids)
    for capsule in capsules:
        for link_type in ['parent', 'children', 'related', 'siblings']:
            for link_id in capsule['links'].get(link_type, []):
                if link_id not in id_set:
                    issues.append(f"Capsule '{capsule['id']}': Invalid {link_type} link to '{link_id}'")
    
    # Check SEO data
    for capsule in capsules:
        seo = capsule.get('seo', {})
        if not seo.get('title'):
            issues.append(f"Capsule '{capsule['id']}': Missing SEO title")
        if not seo.get('description'):
            issues.append(f"Capsule '{capsule['id']}': Missing SEO description")
        if not seo.get('keywords') or len(seo['keywords']) == 0:
            issues.append(f"Capsule '{capsule['id']}': Missing SEO keywords")
    
    # Check content
    for capsule in capsules:
        content = capsule.get('content', '')
        if not content:
            issues.append(f"Capsule '{capsule['id']}': Empty content")
        elif len(content) < 100:
            issues.append(f"Capsule '{capsule['id']}': Content too short ({len(content)} chars)")
    
    # Print results
    if issues:
        print(f"❌ Found {len(issues)} issues:\n")
        for issue in issues[:20]:
            print(f"  - {issue}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more issues")
        return False, issues
    else:
        print(f"✅ All {len(capsules)} capsules are valid!")
        return True, []

if __name__ == '__main__':
    success, issues = validate_capsules()
    sys.exit(0 if success else 1)
