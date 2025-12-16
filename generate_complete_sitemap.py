from datetime import datetime
import xml.etree.ElementTree as ET

def create_sitemap(input_file='blog_urls.txt', output_file='complete-sitemap.xml'):
    """Generate XML sitemap from URL list"""
    
    # Read URLs from file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Read all lines and strip whitespace
            all_lines = f.readlines()
            # Keep URLs, remove empty lines but keep track of what we're filtering
            urls = []
            empty_count = 0
            for line in all_lines:
                stripped = line.strip()
                if stripped:
                    urls.append(stripped)
                else:
                    empty_count += 1
        
        print(f"Read {len(all_lines)} total lines from {input_file}")
        print(f"Found {len(urls)} valid URLs")
        if empty_count > 0:
            print(f"Filtered out {empty_count} empty lines")
        
    except FileNotFoundError:
        print(f"ERROR: {input_file} not found!")
        print("Make sure the file is in the same directory as this script.")
        return 0
    except Exception as e:
        print(f"ERROR reading file: {e}")
        return 0
    
    if len(urls) == 0:
        print("ERROR: No URLs found in file!")
        return 0
    
    # Create XML structure
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add each URL to sitemap
    for url in urls:
        url_element = ET.SubElement(urlset, 'url')
        
        # Add location (required)
        loc = ET.SubElement(url_element, 'loc')
        loc.text = url
        
        # Add last modified date (today)
        lastmod = ET.SubElement(url_element, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
        
        # Add change frequency
        changefreq = ET.SubElement(url_element, 'changefreq')
        if '/blog/' in url.lower():
            changefreq.text = 'monthly'
        else:
            changefreq.text = 'weekly'
        
        # Add priority
        priority = ET.SubElement(url_element, 'priority')
        if url.endswith('.com') or url.endswith('.com/'):
            priority.text = '1.0'  # Homepage
        elif '/blog/' in url.lower():
            priority.text = '0.8'  # Blog posts
        else:
            priority.text = '0.9'  # Other main pages
    
    # Create tree and format with indentation
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    
    # Write to file with XML declaration
    try:
        with open(output_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding='utf-8', xml_declaration=False)
        
        print(f"\n{'='*70}")
        print(f"SUCCESS! Sitemap created: {output_file}")
        print(f"{'='*70}")
        print(f"Total URLs in sitemap: {len(urls)}")
        print(f"\nYou can now upload this file to GitHub.")
        print(f"{'='*70}")
        
        return len(urls)
        
    except Exception as e:
        print(f"ERROR writing sitemap: {e}")
        return 0

if __name__ == "__main__":
    print("="*70)
    print("COMPLETE SITEMAP GENERATOR")
    print("="*70)
    print()
    
    count = create_sitemap()
    
    if count > 0:
        print(f"\nNext step: Upload 'complete-sitemap.xml' to GitHub")
    else:
        print("\nSitemap generation failed. Check errors above.")
