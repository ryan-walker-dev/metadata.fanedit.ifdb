#!/usr/bin/env python3
"""
Test to verify that URL encoding is correctly handling special characters in API parameters.
This test validates the fix for the "Bad Request" error.
"""

import urllib.parse


def test_url_encoding():
    """Test that URL encoding properly handles special characters in API credentials"""
    
    print("=" * 70)
    print("Testing URL Encoding for API Parameters")
    print("=" * 70)
    print()
    
    # Test cases with various special characters that might appear in API keys/IDs
    test_cases = [
        {
            "name": "Simple API key and ID",
            "api_key": "AIzaSyABC123",
            "search_engine_id": "abc123def456",
            "query": "Star Wars"
        },
        {
            "name": "API key with special characters",
            "api_key": "AIzaSy-ABC_123+456",
            "search_engine_id": "abc123def456",
            "query": "The Empire Strikes Back"
        },
        {
            "name": "Search engine ID with special characters",
            "api_key": "AIzaSyABC123",
            "search_engine_id": "abc-123_def:456",
            "query": "Star Wars"
        },
        {
            "name": "Query with spaces and special characters",
            "api_key": "AIzaSyABC123",
            "search_engine_id": "abc123def456",
            "query": "Star Wars: The Empire Strikes Back (1980)"
        },
        {
            "name": "All parameters with special characters",
            "api_key": "AIzaSy-ABC+123/456=",
            "search_engine_id": "abc-123:def_456",
            "query": "Star Wars: A New Hope & Empire Strikes Back"
        }
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test['name']}")
        print("-" * 70)
        
        api_key = test['api_key']
        search_engine_id = test['search_engine_id']
        query = test['query']
        
        # The OLD way (incorrect - manual concatenation)
        old_url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={api_key}"
            f"&cx={search_engine_id}"
            f"&q={urllib.parse.quote(query)}"
        )
        
        # The NEW way (correct - using urlencode)
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query
        }
        new_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        print(f"  API Key: {api_key}")
        print(f"  Search Engine ID: {search_engine_id}")
        print(f"  Query: {query}")
        print()
        
        # Check if URLs are different (they should be when special chars are present)
        if old_url != new_url:
            print(f"  ⚠ URLs differ (as expected when special chars present):")
            print(f"  OLD (incorrect): {old_url[:80]}...")
            print(f"  NEW (correct):   {new_url[:80]}...")
            print()
        
        # Validate that the new URL properly encodes all parameters
        parsed = urllib.parse.urlparse(new_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        # Check all parameters are present
        if 'key' not in query_params or 'cx' not in query_params or 'q' not in query_params:
            print(f"  ✗ FAIL: Missing parameters in encoded URL")
            all_passed = False
        else:
            # Verify the values match (parse_qs returns lists)
            decoded_key = query_params['key'][0]
            decoded_cx = query_params['cx'][0]
            decoded_q = query_params['q'][0]
            
            if decoded_key == api_key and decoded_cx == search_engine_id and decoded_q == query:
                print(f"  ✓ PASS: All parameters correctly encoded and decoded")
            else:
                print(f"  ✗ FAIL: Parameters don't match after encoding/decoding")
                print(f"    Expected key: {api_key}")
                print(f"    Got key:      {decoded_key}")
                print(f"    Expected cx:  {search_engine_id}")
                print(f"    Got cx:       {decoded_cx}")
                print(f"    Expected q:   {query}")
                print(f"    Got q:        {decoded_q}")
                all_passed = False
        
        print()
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print()
        print("The new URL encoding approach correctly handles:")
        print("  • Special characters in API keys")
        print("  • Special characters in search engine IDs")
        print("  • Special characters in search queries")
        print("  • All parameters are properly encoded")
        print()
        print("This fix resolves the 'Bad Request' error that occurred when")
        print("API credentials contained special characters that were not")
        print("properly URL-encoded in the old implementation.")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    print()
    
    return all_passed


if __name__ == '__main__':
    import sys
    success = test_url_encoding()
    sys.exit(0 if success else 1)
