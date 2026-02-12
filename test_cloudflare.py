#!/usr/bin/env python3
"""
Test script to verify IFDB scraper compatibility with Cloudflare-protected fanedit.org
"""

import urllib.request
import urllib.error
import sys

def test_google_search(query="Mr White Part II"):
    """Test if Google search returns fanedit.org results"""
    print("=" * 70)
    print("TEST 1: Google Search Stage")
    print("=" * 70)
    
    url = f"https://www.google.com/search?hl=en&as_q={query.replace(' ', '+')}&as_sitesearch=https://fanedit.org/"
    print(f"URL: {url}")
    
    try:
        headers = {'User-Agent': 'Kodi/19.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Check for fanedit.org URLs
            if 'fanedit.org' in html:
                print("✅ SUCCESS: Google search returns fanedit.org results")
                
                # Try to extract some URLs
                import re
                urls = re.findall(r'https://fanedit\.org/[^/"]+/', html)
                if urls:
                    print(f"   Found {len(set(urls))} unique fanedit.org URLs")
                    for i, url in enumerate(list(set(urls))[:3], 1):
                        print(f"   {i}. {url}")
                return True
            else:
                print("⚠️  WARNING: No fanedit.org results found")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ FAILED: HTTP Error {e.code}")
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
            
            if 'challenge' in html.lower() or len(html) < 1000:
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
    print("\n" + "=" * 70)
    print("IFDB SCRAPER - CLOUDFLARE COMPATIBILITY TEST")
    print("=" * 70)
    print("\nThis script tests if the IFDB scraper will work with Cloudflare")
    print("protection on fanedit.org\n")
    
    # Run tests
    test1 = test_google_search()
    test2 = test_detail_page()
    test3 = test_pattern_matching() if test2 else False
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"1. Google Search:      {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"2. Detail Page Access: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"3. Pattern Matching:   {'✅ PASS' if test3 else '⚠️  SKIP' if not test2 else '❌ FAIL'}")
    
    print("\n" + "=" * 70)
    if test1 and test2:
        print("✅ SCRAPER SHOULD WORK")
        print("\nThe scraper is compatible with your Cloudflare configuration!")
        print("Both search and detail page access are working correctly.")
    elif test1 and not test2:
        print("⚠️  SCRAPER PARTIALLY WORKING")
        print("\nGoogle search works, but detail pages are blocked by Cloudflare.")
        print("\nTO FIX:")
        print("1. Go to Cloudflare Dashboard → Security → WAF")
        print("2. Create a rule to allow User-Agent containing 'Kodi'")
        print("3. Or lower Security Level to Low/Medium")
        print("\nSee CLOUDFLARE_COMPATIBILITY.md for detailed instructions.")
    else:
        print("❌ SCRAPER MAY NOT WORK")
        print("\nThere are issues accessing the required resources.")
        print("\nTO FIX:")
        print("1. Check your internet connection")
        print("2. Verify fanedit.org is accessible")
        print("3. Check Cloudflare configuration")
    print("=" * 70)
    
    return 0 if (test1 and test2) else 1

if __name__ == "__main__":
    sys.exit(main())
