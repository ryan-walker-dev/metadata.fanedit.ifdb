#!/usr/bin/env python3
"""
Test script to verify Google Custom Search API connection
and URL construction for the IFDB scraper
"""

import urllib.request
import urllib.parse
import json
import sys
from urllib.parse import urlparse

def test_api_connection(api_key, search_engine_id, query="The Empire Strikes Back"):
    """Test the Google Custom Search API connection"""
    
    print("=" * 70)
    print("IFDB Scraper - Google Custom Search API Connection Test")
    print("=" * 70)
    print()
    
    # Construct the URL exactly as the scraper does
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    print(f"Test Query: {query}")
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"Search Engine ID: {search_engine_id}")
    print()
    print(f"Constructed URL:")
    print(f"{url}")
    print()
    print("-" * 70)
    
    # Try to connect
    print("Attempting to connect to Google Custom Search API...")
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Kodi/20.0 (X11; Linux x86_64) App_Bitness/64 Version/20.0-Git:20171217-nogitfound')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            data = response.read().decode('utf-8')
            
            print(f"✓ Connection successful! (Status: {status_code})")
            print()
            
            # Parse JSON response
            try:
                json_data = json.loads(data)
                
                # Check for API errors
                if 'error' in json_data:
                    error_info = json_data['error']
                    print(f"✗ API Error:")
                    print(f"  Code: {error_info.get('code')}")
                    print(f"  Message: {error_info.get('message')}")
                    print(f"  Status: {error_info.get('status')}")
                    return False
                
                # Check for search results
                if 'items' in json_data:
                    items = json_data['items']
                    print(f"✓ Found {len(items)} search results:")
                    print()
                    for i, item in enumerate(items[:3], 1):
                        title = item.get('title', 'No title')
                        link = item.get('link', 'No link')
                        print(f"  {i}. {title}")
                        print(f"     {link}")
                        print()
                    
                    # Check if any results are from fanedit.org (using proper URL parsing)
                    fanedit_results = []
                    for item in items:
                        link = item.get('link', '')
                        if link:
                            parsed = urlparse(link)
                            # Check if domain is exactly fanedit.org or a subdomain
                            if parsed.netloc == 'fanedit.org' or parsed.netloc.endswith('.fanedit.org'):
                                fanedit_results.append(item)
                    
                    if fanedit_results:
                        print(f"✓ Found {len(fanedit_results)} results from fanedit.org")
                        return True
                    else:
                        print("✗ No results from fanedit.org found")
                        print("  This may indicate the custom search engine is not configured correctly")
                        return False
                else:
                    print("✗ No search results found")
                    print(f"  Response keys: {list(json_data.keys())}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"✗ Failed to parse JSON response: {e}")
                print(f"  Response preview: {data[:500]}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error: {e.code}")
        print(f"  Message: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            error_data = json.loads(error_body)
            if 'error' in error_data:
                error_info = error_data['error']
                print(f"  API Error: {error_info.get('message')}")
        except:
            pass
        return False
        
    except urllib.error.URLError as e:
        print(f"✗ URL Error: {e.reason}")
        return False
        
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
        return False

def main():
    """Main function"""
    print()
    
    # For testing purposes, use placeholder values
    # Users should replace these with their actual credentials
    api_key = "YOUR_API_KEY_HERE"
    search_engine_id = "YOUR_SEARCH_ENGINE_ID_HERE"
    
    if len(sys.argv) >= 3:
        api_key = sys.argv[1]
        search_engine_id = sys.argv[2]
        query = sys.argv[3] if len(sys.argv) >= 4 else "The Empire Strikes Back"
    
    if api_key == "YOUR_API_KEY_HERE" or search_engine_id == "YOUR_SEARCH_ENGINE_ID_HERE":
        print("ERROR: Please provide your API credentials")
        print()
        print("Usage:")
        print(f"  python3 {sys.argv[0]} <api_key> <search_engine_id> [search_query]")
        print()
        print("Example:")
        print(f"  python3 {sys.argv[0]} AIzaSyABC123... c4204d1b86cc34a32 'Star Wars'")
        print()
        return 1
    
    success = test_api_connection(api_key, search_engine_id)
    
    print()
    print("=" * 70)
    if success:
        print("✓ TEST PASSED: API connection is working correctly")
        print("  The scraper should be able to connect successfully")
    else:
        print("✗ TEST FAILED: API connection has issues")
        print("  Please check your API credentials and configuration")
    print("=" * 70)
    print()
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
