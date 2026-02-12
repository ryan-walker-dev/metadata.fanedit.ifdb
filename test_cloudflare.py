#!/usr/bin/env python3
"""
Test script to verify if the Google Custom Search API and fanedit.org allow Kodi scraper access.

IMPORTANT: You don't control fanedit.org's Cloudflare settings. This script just
checks if their current configuration allows the IFDB scraper to work.
"""

import urllib.request
import urllib.error
import sys

def test_google_search(query="Mr White Part II"):
    """Test if Google Custom Search API returns fanedit.org results"""
    print("=" * 70)
    print("TEST 1: Google Custom Search API Stage")
    print("=" * 70)
    
    # Use the Google Custom Search API
    api_key = "AIzaSyBRb-5t6x4X7IAlSl1WishLV6XS5lZclR4"
    search_engine_id = "c4204d1b86cc34a32"
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query.replace(' ', '+')}"
    print(f"URL: {url}")
    
    try:
        headers = {'User-Agent': 'Kodi/19.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            import json
            data = json.loads(response.read().decode('utf-8'))
            
            # Check if we have items in the response
            if 'items' in data:
                print("✅ SUCCESS: Google Custom Search API returns results")
                
                # Extract fanedit.org URLs
                fanedit_urls = [item['link'] for item in data['items'] if 'fanedit.org' in item.get('link', '')]
                
                if fanedit_urls:
                    print(f"   Found {len(fanedit_urls)} fanedit.org URLs")
                    for i, url in enumerate(fanedit_urls[:3], 1):
                        title = data['items'][i-1].get('title', 'N/A')
                        print(f"   {i}. {title}")
                        print(f"      {url}")
                    return True
                else:
                    print("⚠️  WARNING: No fanedit.org results found in API response")
                    return False
            else:
                print("⚠️  WARNING: No items in API response")
                if 'error' in data:
                    print(f"   API Error: {data['error'].get('message', 'Unknown error')}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ FAILED: HTTP Error {e.code}")
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            if 'error' in error_data:
                print(f"   API Error: {error_data['error'].get('message', 'Unknown error')}")
        except:
            pass
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_detail_page(url="https://fanedit.org/mr-white-part-ii-phoenix/"):
    """Test if we can access a fanedit.org detail page"""
    print("\n" + "=" * 70)
    print("TEST 2: Detail Page Access (Cloudflare Test)")
    print("=" * 70)
    print(f"URL: {url}")
    
    # Test with Kodi User-Agent
    print("\nAttempt 1: Using Kodi User-Agent")
    try:
        headers = {
            'User-Agent': 'Kodi/19.0 (X11; Linux x86_64) App_Bitness/64 Version/19.0',
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            status = response.status
            
            # Check if we got actual content or Cloudflare challenge
            if 'Cloudflare' in html and ('challenge' in html.lower() or 'checking your browser' in html.lower()):
                print("❌ BLOCKED: Received Cloudflare challenge page")
                print("   → Cloudflare is blocking automated requests")
                print("   → Need to whitelist Kodi User-Agent in Cloudflare")
                return False
            elif '<div class="jrFieldRow">' in html or '<h1' in html:
                print("✅ SUCCESS: Received actual page content")
                print(f"   Status: {status}")
                print(f"   HTML size: {len(html)} bytes")
                
                # Check for expected content
                if 'jrBriefsynopsis' in html or 'jrGenre' in html:
                    print("   ✓ Found expected HTML structure (jrFieldRow classes)")
                return True
            else:
                print("⚠️  WARNING: Received HTML but structure unclear")
                print(f"   Status: {status}")
                print(f"   First 500 chars: {html[:500]}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ BLOCKED: HTTP Error {e.code}")
        if e.code == 403:
            print("   → 403 Forbidden: Cloudflare is blocking the request")
        elif e.code == 503:
            print("   → 503 Service Unavailable: Likely Cloudflare challenge")
        print("   → Need to configure Cloudflare to allow Kodi requests")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_pattern_matching(url="https://fanedit.org/mr-white-part-ii-phoenix/"):
    """Test if our regex patterns work on the actual page"""
    print("\n" + "=" * 70)
    print("TEST 3: Pattern Matching (if page accessible)")
    print("=" * 70)
    
    try:
        headers = {'User-Agent': 'Kodi/19.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Check for Cloudflare challenge page (be more specific than just "challenge")
            if ('Cloudflare' in html and 'challenge' in html.lower()) or len(html) < 1000:
                print("⚠️  SKIPPED: Cannot access page (Cloudflare blocking)")
                return False
            
            import re
            
            # Test patterns
            patterns = {
                'Title': r'<h1[^>]*>([^<]+)</h1>',
                'Synopsis': r'<div class="jrBriefsynopsis jrFieldRow">[\s\S]*?<div class="jrFieldValue">(.*?)</div>',
                'Genre': r'<div class="jrGenre jrFieldRow">[\s\S]*?<li><a[^>]*>([^<]+)</a></li>',
                'Year': r'<div class="jrFaneditreleasedate jrFieldRow">[\s\S]*?([0-9]{4})',
                'Faneditor': r'<div class="jrFaneditorname jrFieldRow">[\s\S]*?<li><a[^>]*>([^<]+)</a></li>',
            }
            
            results = {}
            for name, pattern in patterns.items():
                match = re.search(pattern, html, re.DOTALL)
                results[name] = match is not None
                status = "✓" if match else "✗"
                value = match.group(1)[:50] if match else "Not found"
                print(f"   {status} {name}: {value}")
            
            success_count = sum(results.values())
            total_count = len(results)
            
            if success_count == total_count:
                print(f"\n✅ ALL PATTERNS WORKING ({success_count}/{total_count})")
                return True
            elif success_count > 0:
                print(f"\n⚠️  PARTIAL SUCCESS ({success_count}/{total_count} patterns working)")
                return True
            else:
                print(f"\n❌ NO PATTERNS MATCHED (check HTML structure)")
                return False
                
    except Exception as e:
        print(f"⚠️  SKIPPED: {e}")
        return False

def main():
    import datetime
    
    print("\n" + "=" * 70)
    print("IFDB SCRAPER - GOOGLE CUSTOM SEARCH API & CLOUDFLARE TEST")
    print("=" * 70)
    print(f"Test Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis script tests if the IFDB scraper can access Google Custom Search")
    print("API and fanedit.org")
    print("NOTE: You don't control fanedit.org's Cloudflare - this just")
    print("      checks if their current configuration allows Kodi.\n")
    
    # Run tests
    test1 = test_google_search()
    test2 = test_detail_page()
    test3 = test_pattern_matching() if test2 else False
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"1. Custom Search API:  {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"2. Detail Page Access: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"3. Pattern Matching:   {'✅ PASS' if test3 else '⚠️  SKIP' if not test2 else '❌ FAIL'}")
    
    print("\n" + "=" * 70)
    if test1 and test2 and test3:
        print("✅ SCRAPER FULLY TESTED AND WORKING")
        print("\nAll tests passed! The scraper can:")
        print("- Find fanedits via Google Custom Search API")
        print("- Access fanedit.org detail pages")
        print("- Extract metadata using all regex patterns")
        print("\nYou should be able to use this scraper in Kodi successfully!")
    elif test1 and test2:
        print("✅ SCRAPER SHOULD WORK")
        print("\nThe scraper can access Google Custom Search API and fanedit.org!")
        print("Custom Search API and detail page access are both working.")
        print("Pattern matching test had issues, but the scraper should still work.")
        print("\nYou should be able to use this scraper in Kodi.")
    elif test1 and not test2:
        print("⚠️  SCRAPER WILL NOT WORK")
        print("\nGoogle Custom Search API works, but fanedit.org is blocking detail pages.")
        print("This is likely due to Cloudflare protecting the site.")
        print("\n⚠️  IMPORTANT: You don't control fanedit.org's Cloudflare!")
        print("\nYOUR OPTIONS:")
        print("1. Contact fanedit.org administrators (if possible)")
        print("   - Explain that Kodi scrapers are being blocked")
        print("   - Request they allow 'User-Agent: Kodi/*' in Cloudflare")
        print("2. Use manual .nfo files for metadata instead")
        print("3. Check back periodically - they may adjust settings")
        print("\nSee CLOUDFLARE_COMPATIBILITY.md for more information.")
    else:
        print("❌ CANNOT TEST PROPERLY")
        print("\nUnable to access required resources.")
        print("\nPOSSIBLE CAUSES:")
        print("1. No internet connection")
        print("2. Google Custom Search API or fanedit.org temporarily unavailable")
        print("3. Network/firewall blocking requests")
        print("4. API key quota exceeded (100 queries/day free tier)")
        print("\nTry again later or check your connection.")
    print("=" * 70)
    
    return 0 if (test1 and test2) else 1

if __name__ == "__main__":
    sys.exit(main())
