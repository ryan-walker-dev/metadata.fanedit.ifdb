# Cloudflare Protection Compatibility

## How the Scraper Works with Cloudflare

The IFDB scraper uses a **two-stage process** to retrieve movie information:

### Stage 1: Search via Google ✅
```
User searches for "Mr White Part II" in Kodi
  ↓
Kodi requests: https://www.google.com/search?hl=en&as_q=Mr+White+Part+II&as_sitesearch=https://fanedit.org/
  ↓
Google returns search results with fanedit.org URLs
  ↓
Scraper extracts URLs from Google's HTML (e.g., https://fanedit.org/mr-white-part-ii-phoenix/)
```

**Cloudflare Impact**: ✅ **No impact** - Google can access fanedit.org because it's a legitimate search engine crawler that needs to be allowed for SEO.

### Stage 2: Fetch Detail Page ⚠️
```
Kodi has the URL: https://fanedit.org/mr-white-part-ii-phoenix/
  ↓
Kodi requests the page directly from fanedit.org
  ↓
Cloudflare checks the request
  ↓
If allowed: Returns HTML → Scraper extracts metadata ✅
If blocked: Returns challenge page → Scraper fails ❌
```

**Cloudflare Impact**: ⚠️ **Potential issue** - Depends on Cloudflare configuration

## Will It Work?

### ✅ YES, if:
1. **Cloudflare allows Kodi's User-Agent** 
   - Kodi typically identifies itself as: `Kodi/[version]`
   - If your firewall exception allows this User-Agent, it will work

2. **Cloudflare security level is Low/Medium**
   - Challenge pages are only shown for suspicious traffic
   - Legitimate scrapers are usually allowed

3. **You've whitelisted Kodi/bot traffic**
   - You mentioned adding a "firewall exception" - if this includes:
     - Specific User-Agents (Kodi/*)
     - Specific IP ranges
     - Bot/scraper traffic category
   - Then it should work fine

### ❌ NO, if:
1. **Cloudflare blocks all automated requests**
   - "Under Attack Mode" or "I'm Under Attack Mode"
   - Shows JavaScript challenge to all non-browser traffic
   - Kodi scrapers cannot solve JavaScript challenges

2. **Strict bot detection is enabled**
   - Blocks any automated User-Agent
   - Requires browser fingerprinting
   - Requires cookies/sessions

## How to Verify

### Test 1: Check if Google can find results
```bash
# If this returns results, Stage 1 works ✅
curl "https://www.google.com/search?q=site:fanedit.org+Mr+White"
```

### Test 2: Check if Kodi can access detail pages
```bash
# Simulate Kodi's request
curl -A "Kodi/19.0" "https://fanedit.org/mr-white-part-ii-phoenix/"

# If you get:
# - HTML with actual content → ✅ Will work
# - Cloudflare challenge page → ❌ Needs configuration
# - 403 Forbidden → ❌ Needs configuration
```

### Test 3: Check from Kodi directly
1. Install the scraper in Kodi
2. Try to scrape a movie
3. Check Kodi's log file (`kodi.log`) for errors like:
   - `403 Forbidden` - Cloudflare is blocking
   - `503 Service Unavailable` - Challenge page
   - Success - See parsed metadata

## Recommended Cloudflare Settings

To ensure the scraper works reliably, configure Cloudflare to:

### Option 1: Whitelist Kodi User-Agent (Recommended)
```
Cloudflare Dashboard → Security → WAF
→ Create WAF Rule:
   - Field: User-Agent
   - Operator: contains
   - Value: "Kodi"
   - Action: Allow
```

### Option 2: Whitelist Bot Traffic Category
```
Cloudflare Dashboard → Security → Bots
→ Configure Bot Fight Mode
→ Allow "Verified Bots" category
```

### Option 3: Lower Security Level for Scrapers
```
Cloudflare Dashboard → Security → Settings
→ Security Level: Low or Medium (not High)
→ Challenge Passage: 30 minutes or more
```

## Rate Limiting Considerations

Even with Cloudflare configured correctly, consider:

1. **Kodi makes multiple requests per search**
   - 1 request to Google
   - 1+ requests to fanedit.org for each result
   - 1 request per selected movie for details

2. **Bulk scraping**
   - When users scan entire movie libraries
   - Can generate 100+ requests in minutes
   - May trigger rate limiting

3. **Recommendation**
   - Set Cloudflare rate limits reasonably (e.g., 60 requests/minute per IP)
   - Don't use "Under Attack Mode" permanently
   - Monitor logs for false positives

## Current Implementation Status

✅ **Search method**: Uses Google (bypasses Cloudflare for search)
✅ **Detail extraction**: Updated regex patterns for current HTML structure
✅ **Multi-line matching**: Uses `[\s\S]*?` for reliability
✅ **URL handling**: Full URLs from Google results

⚠️ **Cloudflare compatibility**: Depends on your configuration

## Next Steps

1. **Test the scraper** with a movie search in Kodi
2. **Check Cloudflare logs** in the Dashboard to see if requests are being blocked
3. **Adjust Cloudflare rules** if needed using the recommendations above
4. **Monitor** the first few days for any issues

## Summary

**Short answer**: Yes, it should work if your firewall exception allows Kodi's User-Agent or bot traffic. The Google search stage will always work, and the detail page fetching will work if Cloudflare permits the requests.

**Best practice**: Configure Cloudflare to explicitly allow `User-Agent: Kodi/*` requests to ensure reliability.
