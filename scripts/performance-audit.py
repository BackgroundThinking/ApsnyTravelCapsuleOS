#!/usr/bin/env python3
"""
Performance Audit Script
Analyzes the application for performance issues and provides recommendations
"""

import json
import os
from pathlib import Path

def analyze_performance():
    """Analyze application performance metrics"""
    
    print("=" * 70)
    print("ApsnyTravelCapsuleOS - Performance Audit")
    print("=" * 70)
    print()
    
    # 1. Bundle Size Analysis
    print("📦 BUNDLE SIZE ANALYSIS")
    print("-" * 70)
    
    dist_path = Path("dist/public/assets")
    if dist_path.exists():
        total_size = 0
        files = []
        
        for file in dist_path.glob("*"):
            if file.is_file():
                size = file.stat().st_size
                total_size += size
                files.append((file.name, size))
        
        files.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Total Bundle Size: {total_size / 1024:.2f} KB")
        print(f"Number of Files: {len(files)}\n")
        print("Top Files by Size:")
        for name, size in files[:5]:
            print(f"  {name}: {size / 1024:.2f} KB")
    else:
        print("⚠️  Build directory not found. Run 'pnpm build' first.")
    
    # 2. Data File Analysis
    print("\n📊 DATA FILE ANALYSIS")
    print("-" * 70)
    
    data_files = [
        ("client/public/capsules.json", "Capsules Data"),
        ("client/public/search-index.json", "Search Index"),
        ("client/public/structured-data.json", "Structured Data"),
        ("client/public/sitemap.xml", "Sitemap"),
    ]
    
    total_data_size = 0
    for file_path, label in data_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            total_data_size += size
            print(f"{label}: {size / 1024:.2f} KB")
    
    print(f"\nTotal Data Size: {total_data_size / 1024:.2f} KB")
    
    # 3. Content Analysis
    print("\n📝 CONTENT ANALYSIS")
    print("-" * 70)
    
    with open("client/public/capsules.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    capsules = data["capsules"]
    
    total_content = sum(len(c.get("content", "")) for c in capsules)
    avg_content = total_content // len(capsules) if capsules else 0
    
    print(f"Total Capsules: {len(capsules)}")
    print(f"Total Content Size: {total_content / 1024:.2f} KB")
    print(f"Average Content per Capsule: {avg_content:,} characters")
    
    # 4. Performance Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 70)
    
    recommendations = []
    
    # Check bundle size
    if total_size > 600 * 1024:
        recommendations.append("• Consider implementing code splitting for large bundles")
    
    # Check data size
    if total_data_size > 500 * 1024:
        recommendations.append("• Consider compressing data files (gzip)")
    
    # Check content size
    if avg_content > 5000:
        recommendations.append("• Consider lazy loading content or pagination")
    
    if not recommendations:
        recommendations.append("✅ Application is well-optimized!")
    
    for rec in recommendations:
        print(rec)
    
    print("\n" + "=" * 70)
    print("Audit Complete")
    print("=" * 70)

if __name__ == "__main__":
    analyze_performance()
