# metadata.fanedit.ifdb
Kodi Movie Information Scraper for the Internet Fanedit Database using Google Custom Search API to search (due to the limitation of IFDB's search)

Metadata agent for scraping information from the Internet Fanedit Database (IFDB) at https://fanedit.org/

Scraper will use Google Custom Search API to search and then fetch details from fanedit.org

## Features
- Uses Google Custom Search API to find fanedits (bypasses direct site search issues and anti-bot measures)
- Extracts complete metadata: title, synopsis, genres, faneditor, year, poster
- Works with the current fanedit.org HTML structure (2023+)

## Installation
1. Place "metadata.fanedit.ifdb" folder in `~Kodi install dir~/addons` OR Create a Zip with all files in this repository and use "Install From Zip File"
3. In Kodi, choose IFDB as the information source for your movie section
4. Scraper will use Google Custom Search API to search and then fetch details from fanedit.org

## API Configuration
This scraper uses the Google Custom Search API to find fanedits. The API credentials are pre-configured:
- **API Key**: Built-in (100 queries per day free tier)
- **Search Engine ID**: Configured to search fanedit.org
- **Search Engine URL**: https://cse.google.com/cse?cx=c4204d1b86cc34a32

The free tier limit is 100 queries per day, which is sufficient for typical usage. If you need more queries, you can create your own Google Custom Search API credentials and modify the `ifdb.xml` file.

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
