# metadata.fanedit.ifdb
Kodi Movie Information Scraper for the Internet Fanedit Database

Metadata agent for scraping information from the Internet Fanedit Database (IFDB) at https://fanedit.org/

## Features
- Uses Google search to find fanedits (bypasses direct site search issues)
- Extracts complete metadata: title, synopsis, genres, faneditor, year, poster
- Works with the current fanedit.org HTML structure (2023+)

## Installation
1. Place "metadata.fanedit.ifdb" folder in `~Kodi install dir~/addons`
2. In Kodi, choose IFDB as the information source for your movie section
3. Scraper will use Google to search and then fetch details from fanedit.org

## Cloudflare Compatibility

**Important**: fanedit.org is protected by Cloudflare. You don't control their Cloudflare settings, so whether the scraper works depends on how they've configured it.

### How it works:
- ✅ **Google Search**: Always works (Google is whitelisted for SEO)
- ⚠️ **Detail Pages**: Depends on fanedit.org allowing Kodi's User-Agent

### Testing:
```bash
# Test if scraper can currently access fanedit.org
python3 test_cloudflare.py
```

### If the scraper doesn't work:
1. Run the test script above to confirm it's being blocked
2. You may need to contact fanedit.org administrators
3. Alternative: Use manual `.nfo` files for metadata

See **[CLOUDFLARE_COMPATIBILITY.md](CLOUDFLARE_COMPATIBILITY.md)** for detailed information about:
- Why Cloudflare might block the scraper
- What you can and cannot do about it
- How to test and monitor the situation
- Alternative solutions if blocked

## Testing
```bash
# Test if scraper can access fanedit.org with Cloudflare
python3 test_cloudflare.py
```

## Requirements
- Kodi 17+ (Krypton or later)
- Internet connection
- fanedit.org must allow Kodi User-Agent (you cannot control this - it depends on their Cloudflare configuration)

## Notes
- This scraper accesses fanedit.org which is not under your control
- If fanedit.org's Cloudflare blocks Kodi, the scraper cannot work
- Test with `python3 test_cloudflare.py` to check current access status
