# Cloudflare Protection Compatibility

## Important: You Don't Control fanedit.org's Cloudflare

**This scraper accesses fanedit.org, which is protected by Cloudflare. You (the user) have no control over fanedit.org's Cloudflare settings.** Whether the scraper works depends on how the fanedit.org administrators have configured their Cloudflare protection.

## How the Scraper Works with Cloudflare

The IFDB scraper uses a **two-stage process** to retrieve movie information:

### Stage 1: Search via Google ✅ ALWAYS WORKS
```
User searches for "Mr White Part II" in Kodi
  ↓
Kodi requests: https://www.google.com/search?hl=en&as_q=Mr+White+Part+II&as_sitesearch=https://fanedit.org/
  ↓
Google returns search results with fanedit.org URLs
  ↓
Scraper extracts URLs from Google's HTML (e.g., https://fanedit.org/mr-white-part-ii-phoenix/)
```

**Cloudflare Impact**: ✅ **No impact** - Google can access fanedit.org because it's a legitimate search engine crawler that must be allowed for SEO.

### Stage 2: Fetch Detail Page ⚠️ DEPENDS ON SITE CONFIG
```
Kodi has the URL: https://fanedit.org/mr-white-part-ii-phoenix/
  ↓
Kodi requests the page directly from fanedit.org
  ↓
Cloudflare checks the request based on fanedit.org's configuration
  ↓
If fanedit.org allows Kodi: Returns HTML → Scraper extracts metadata ✅
If fanedit.org blocks Kodi: Returns challenge page → Scraper fails ❌
```

**Cloudflare Impact**: ⚠️ **Outside your control** - Depends on how fanedit.org administrators configured Cloudflare

## Will It Work?

**The short answer: It depends on fanedit.org's Cloudflare configuration, which you don't control.**

### ✅ It WILL work if fanedit.org:
1. **Allows Kodi's User-Agent** 
   - Kodi identifies itself as: `Kodi/[version]`
   - If fanedit.org's Cloudflare allows this, scraper works

2. **Has reasonable security settings**
   - Not using "Under Attack Mode" permanently
   - Security level is Low/Medium
   - Allows legitimate bot/scraper traffic

3. **Whitelists useful bots**
   - Many sites allow media scrapers for user convenience
   - Similar to allowing RSS readers or API clients

### ❌ It will NOT work if fanedit.org:
1. **Blocks all automated requests**
   - "Under Attack Mode" or "I'm Under Attack Mode" enabled
   - Shows JavaScript challenge to all non-browser traffic
   - Kodi scrapers cannot solve JavaScript challenges

2. **Blocks Kodi specifically**
   - Has rules blocking the Kodi User-Agent
   - Only allows major browsers

3. **Requires browser features**
   - Requires cookies/sessions across multiple requests
   - Requires JavaScript execution
   - Uses advanced bot detection

## What YOU Can Do

Since you don't control fanedit.org's Cloudflare, your options are:

### 1. Test if it works (Recommended)
Use the included test script to check current status:
```bash
python3 test_cloudflare.py
```

This will tell you if the scraper can currently access fanedit.org.

### 2. Monitor and report issues
- If the scraper stops working, it may be due to Cloudflare changes on fanedit.org
- You could report issues to fanedit.org administrators (if they have a contact method)
- They may not be aware their Cloudflare is blocking legitimate users

### 3. Use alternative methods (if blocked)
If Cloudflare blocks the scraper:
- **Manual NFO files**: Create `.nfo` files with metadata manually
- **Contact fanedit.org**: Request they allowlist Kodi User-Agent
- **Wait**: They may adjust settings over time

### 4. What you CANNOT do
- ❌ You cannot configure fanedit.org's Cloudflare settings
- ❌ You cannot bypass Cloudflare's JavaScript challenges
- ❌ You cannot force the scraper to work if fanedit.org blocks it

## How to Verify

### Test if the scraper currently works
```bash
python3 test_cloudflare.py
```

This script tests:
1. ✅ Google search (always works)
2. ⚠️ Detail page access from fanedit.org (depends on their Cloudflare)
3. ✅ Pattern matching on HTML (if accessible)

**What the results mean:**
- **All tests pass**: ✅ Scraper should work in Kodi!
- **Google works, detail pages blocked**: ⚠️ fanedit.org's Cloudflare is blocking Kodi
- **All tests fail**: Check your internet connection

### Understanding the test output

```bash
# If you see this - scraper will work! ✅
✅ SUCCESS: Received actual page content
✓ Found expected HTML structure (jrFieldRow classes)

# If you see this - fanedit.org is blocking ❌
❌ BLOCKED: Received Cloudflare challenge page
→ Cloudflare is blocking automated requests

# If you see this - fanedit.org is blocking ❌
❌ BLOCKED: HTTP Error 403
→ 403 Forbidden: Cloudflare is blocking the request
```

## If fanedit.org is Blocking the Scraper

### You have limited options since you don't control their site:

**1. Report the issue to fanedit.org**
- Look for contact information on fanedit.org
- Explain that Kodi users can't scrape metadata
- Request they allow `User-Agent: Kodi/*` through Cloudflare
- They may not be aware of the issue

**2. Use manual metadata**
- Create `.nfo` files manually with movie information
- Kodi can read these instead of scraping
- Time-consuming but always works

**3. Check periodically**
- fanedit.org may adjust their Cloudflare settings over time
- Run `python3 test_cloudflare.py` occasionally to check
- If they lower security or whitelist Kodi, scraper will start working

**4. Community support**
- Check fanedit.org forums or community
- Other Kodi users may have found workarounds
- Collective requests to the site admins may help

### What fanedit.org admins COULD do (if contacted)

If you can reach fanedit.org administrators, this is what they could configure in Cloudflare to allow the scraper:

```
Cloudflare Dashboard → Security → WAF
→ Create WAF Rule:
   - Field: User-Agent
   - Operator: contains
   - Value: "Kodi"
   - Action: Allow
```

Or:
```
Cloudflare Dashboard → Security → Settings
→ Security Level: Low or Medium (not High)
→ Bot Fight Mode: Allow verified bots
```

**But remember**: This is just information you could share with them. You cannot make these changes yourself.

## Rate Limiting Considerations

Even if fanedit.org allows Kodi, consider:

1. **Kodi makes multiple requests per search**
   - 1 request to Google
   - 1+ requests to fanedit.org for each search result
   - 1 request per selected movie for details

2. **Bulk scraping**
   - When users scan entire movie libraries
   - Can generate 100+ requests in minutes
   - May trigger rate limiting even if initially allowed

3. **Be respectful**
   - Don't hammer the site with excessive requests
   - Use the scraper normally, not for bulk data mining
   - If you notice issues, wait before retrying

## Current Implementation Status

✅ **Search method**: Uses Google (bypasses Cloudflare for search)
✅ **Detail extraction**: Updated regex patterns for current HTML structure
✅ **Multi-line matching**: Uses `[\s\S]*?` for reliability
✅ **URL handling**: Full URLs from Google results

⚠️ **Cloudflare compatibility**: Depends on fanedit.org's configuration (outside your control)

## Summary

**Short answer**: The scraper will work if fanedit.org's Cloudflare allows Kodi's User-Agent. You can test this with `python3 test_cloudflare.py` but you cannot change fanedit.org's settings.

**Current status**: 
- Google search stage: ✅ Always works
- Detail page access: ⚠️ Depends on fanedit.org's Cloudflare (test to find out)

**If blocked**:
- You cannot fix it yourself
- Contact fanedit.org administrators if possible
- Use manual .nfo files as alternative
- Monitor for changes over time

**Best case scenario**: fanedit.org already allows legitimate bots/scrapers, and the scraper works out of the box. Test it to find out!
