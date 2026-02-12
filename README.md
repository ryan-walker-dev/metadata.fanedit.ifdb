# metadata.fanedit.ifdb
Kodi Movie Information Scraper for the Internet Fanedit Database

Metadata agent for scraping information from the Internet Fanedit Database (IFDB) at https://fanedit.org/

## Features
- Uses Google search to find fanedits (bypasses direct site search issues)
- Extracts complete metadata: title, synopsis, genres, faneditor, year, poster
- Works with the current fanedit.org HTML structure (2023+)

## Installation
1. Place "metadata.fanedit.ifdb" folder in `~Kodi install dir~/addons` OR Create a Zip with all files in this repository and use "Install From Zip File"
3. In Kodi, choose IFDB as the information source for your movie section
4. Scraper will use Google to search and then fetch details from fanedit.org

### Testing:
```bash
# Test if scraper can currently access fanedit.org
python3 test_cloudflare.py
```

### If the scraper doesn't work:
1. Run the test script above to confirm if it's being blocked
2. Check if the fanedit.org website format has changed 
3. Alternative: Use manual `.nfo` files for metadata

## Requirements
- Kodi 17+ (Krypton or later)
- Internet connection

## Notes
- If fanedit.org decides to block scraping or the format changes, this scraper will stop working
- Test with `python3 test_cloudflare.py` to check current access status
