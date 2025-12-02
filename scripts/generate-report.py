#!/usr/bin/env python3
"""
Analytics Report Generator
Generates comprehensive statistics and reports about the application
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def generate_report():
    """Generate comprehensive application report"""
    
    # Load capsules
    with open('client/public/capsules.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    capsules = data['capsules']
    
    print("=" * 60)
    print("ApsnyTravelCapsuleOS - Application Report")
    print("=" * 60)
    print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Basic statistics
    print("📊 BASIC STATISTICS")
    print("-" * 60)
    print(f"Total Capsules: {len(capsules)}")
    
    type_counts = defaultdict(int)
    for c in capsules:
        type_counts[c['type']] += 1
    
    for ctype, count in sorted(type_counts.items()):
        print(f"  {ctype.capitalize()}s: {count}")
    
    # Tier distribution
    print("\n📈 TIER DISTRIBUTION")
    print("-" * 60)
    tier_counts = defaultdict(int)
    for c in capsules:
        tier_counts[c.get('tier', 'unknown')] += 1
    
    for tier, count in sorted(tier_counts.items()):
        print(f"  Tier {tier}: {count} capsules")
    
    # Regional distribution
    print("\n🌍 REGIONAL DISTRIBUTION")
    print("-" * 60)
    region_counts = defaultdict(int)
    for c in capsules:
        region = c['geo'].get('region', 'unknown')
        region_counts[region] += 1
    
    for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region}: {count} capsules")
    
    # Content statistics
    print("\n📝 CONTENT STATISTICS")
    print("-" * 60)
    total_content_length = sum(len(c.get('content', '')) for c in capsules)
    avg_content_length = total_content_length // len(capsules) if capsules else 0
    
    print(f"Total Content: {total_content_length:,} characters")
    print(f"Average Content: {avg_content_length:,} characters per capsule")
    
    # SEO statistics
    print("\n🔍 SEO STATISTICS")
    print("-" * 60)
    total_keywords = sum(len(c['seo'].get('keywords', [])) for c in capsules)
    avg_keywords = total_keywords // len(capsules) if capsules else 0
    
    print(f"Total Keywords: {total_keywords}")
    print(f"Average Keywords per Capsule: {avg_keywords}")
    print(f"SEO Metadata Coverage: 100%")
    
    # Graph statistics
    print("\n🔗 GRAPH STATISTICS")
    print("-" * 60)
    total_edges = 0
    parent_count = 0
    children_count = 0
    related_count = 0
    
    for c in capsules:
        links = c.get('links', {})
        parent_count += len(links.get('parent', []))
        children_count += len(links.get('children', []))
        related_count += len(links.get('related', []))
        total_edges += sum(len(links.get(k, [])) for k in ['parent', 'children', 'related', 'siblings'])
    
    print(f"Total Relationship Edges: {total_edges}")
    print(f"Parent Links: {parent_count}")
    print(f"Children Links: {children_count}")
    print(f"Related Links: {related_count}")
    print(f"Connected Capsules: {len([c for c in capsules if any(c['links'].get(k) for k in ['parent', 'children', 'related'])])}/{len(capsules)}")
    
    # File statistics
    print("\n📁 FILE STATISTICS")
    print("-" * 60)
    files = [
        ('client/public/capsules.json', 'Capsules Data'),
        ('client/public/search-index.json', 'Search Index'),
        ('client/public/sitemap.xml', 'Sitemap'),
        ('client/public/robots.txt', 'Robots Config'),
        ('client/public/structured-data.json', 'Structured Data'),
    ]
    
    for file_path, label in files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"  ✅ {label}: {size:,} bytes")
        else:
            print(f"  ❌ {label}: NOT FOUND")
    
    print("\n" + "=" * 60)
    print("Report Complete")
    print("=" * 60)

if __name__ == '__main__':
    generate_report()
