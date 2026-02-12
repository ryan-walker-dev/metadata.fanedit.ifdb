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
Since fanedit.org uses Cloudflare protection, the scraper requires proper configuration:

- ✅ **Google Search**: Always works (Google is whitelisted by Cloudflare for SEO)
- ⚠️ **Detail Pages**: Requires Cloudflare to allow Kodi's User-Agent

### If the scraper isn't working:
1. Verify fanedit.org's Cloudflare is configured to allow `User-Agent: Kodi/*`
2. Check Cloudflare Security Level is not set to "Under Attack Mode"
3. Run the included test: `python3 test_cloudflare.py`

See **[CLOUDFLARE_COMPATIBILITY.md](CLOUDFLARE_COMPATIBILITY.md)** for detailed configuration instructions.

## Testing
```bash
# Test if scraper can access fanedit.org with Cloudflare
python3 test_cloudflare.py
```

## Requirements
- Kodi 17+ (Krypton or later)
- Internet connection
- fanedit.org must be accessible (Cloudflare configured to allow Kodi)
