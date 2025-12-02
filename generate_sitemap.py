#!/usr/bin/env python3
"""
Sitemap Generator for ApsnyTravelCapsuleOS
Generates sitemap.xml, robots.txt, and sitemap-index.xml from capsules.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def generate_sitemaps(capsules_file='client/public/capsules.json', base_url='https://apsnytravel.com'):
    """Generate sitemap files from capsules data"""
    
    # Load capsules
    try:
        with open(capsules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        capsules = data['capsules']
    except FileNotFoundError:
        print(f"❌ Error: {capsules_file} not found")
        return False
    except json.JSONDecodeError:
        print(f"❌ Error: {capsules_file} is not valid JSON")
        return False
    
    print(f"📊 Generating sitemaps for {len(capsules)} capsules...\n")
    
    sitemap_entries = []
    
    # Add main pages
    main_pages = [
        ("", 1.0, "weekly"),
        ("/tours", 0.9, "weekly"),
        ("/places", 0.9, "weekly"),
        ("/guides", 0.9, "weekly"),
    ]
    
    for path, priority, changefreq in main_pages:
        sitemap_entries.append({
            'url': f"{base_url}{path}",
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': changefreq,
            'priority': priority
        })
    
    # Add capsule pages
    for capsule in capsules:
        slug = capsule['slug']
        sitemap_entries.append({
            'url': f"{base_url}/capsule/{slug}",
            'lastmod': capsule.get('metadata', {}).get('updated', datetime.now().strftime('%Y-%m-%d')),
            'changefreq': 'monthly',
            'priority': 0.8 if capsule['type'] == 'product' else 0.7
        })
    
    # Generate sitemap.xml
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for entry in sitemap_entries:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{entry["url"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{entry["lastmod"]}</lastmod>\n'
        sitemap_xml += f'    <changefreq>{entry["changefreq"]}</changefreq>\n'
        sitemap_xml += f'    <priority>{entry["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    # Save sitemap
    sitemap_path = Path('client/public/sitemap.xml')
    sitemap_path.write_text(sitemap_xml, encoding='utf-8')
    print(f"✅ Generated sitemap.xml with {len(sitemap_entries)} entries")
    
    # Generate robots.txt
    robots_txt = f"""# Robots.txt for ApsnyTravel
User-agent: *
Allow: /

# Sitemap
Sitemap: {base_url}/sitemap.xml

# Crawl delay
Crawl-delay: 1
"""
    
    robots_path = Path('client/public/robots.txt')
    robots_path.write_text(robots_txt, encoding='utf-8')
    print(f"✅ Generated robots.txt")
    
    # Generate sitemap-index.xml
    sitemap_index_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{base_url}/sitemap.xml</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
  </sitemap>
</sitemapindex>'''
    
    sitemap_index_path = Path('client/public/sitemap-index.xml')
    sitemap_index_path.write_text(sitemap_index_xml, encoding='utf-8')
    print(f"✅ Generated sitemap-index.xml")
    
    print(f"\n📈 Summary:")
    print(f"  Total URLs: {len(sitemap_entries)}")
    print(f"  Main pages: 4")
    print(f"  Capsule pages: {len(capsules)}")
    
    return True

if __name__ == '__main__':
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'https://apsnytravel.com'
    success = generate_sitemaps(base_url=base_url)
    sys.exit(0 if success else 1)
