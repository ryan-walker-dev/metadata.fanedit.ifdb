# metadata.fanedit.ifdb
Kodi Movie Information Scraper for the Internet Fanedit Database using Google Custom Search API

**Current Version: 1.2.2** - Settings page fixed, improved compatibility with Kodi 17+

Metadata agent for scraping information from the Internet Fanedit Database (IFDB) at https://fanedit.org/

## Recent Updates (v1.2.2)

- ✅ Fixed blank settings page issue
- ✅ Updated settings format for better Kodi compatibility (17+)
- ✅ Added proper language file headers
- ✅ Removed XML parsing issues
- ✅ Improved error handling

See [TESTING.md](TESTING.md) for detailed testing instructions and troubleshooting.

## Features
- Uses Google Custom Search API to find fanedits (bypasses direct site search issues)
- Extracts complete metadata: title, synopsis, genres, faneditor, year, poster
- Works with the current fanedit.org HTML structure (2023+)
- User-configurable API credentials (no hardcoded keys)

## Installation
1. Place "metadata.fanedit.ifdb" folder in `~Kodi install dir~/addons` OR Create a Zip with all files in this repository and use "Install From Zip File"
2. In Kodi, choose IFDB as the information source for your movie section
3. Configure your API credentials (see Configuration section below)

## Configuration

After installing the addon in Kodi:

1. Go to **Settings** → **Media** → **Library**
2. Set content type for your movie folder and select **IFDB** as the scraper
3. Before scraping, configure the addon:
   - Click on **Settings** for the IFDB scraper
   - Enter your **Google API Key**
   - Enter your **Custom Search Engine ID**

### Getting Your API Credentials

#### Step 1: Create a Google Cloud Project and Get an API Key
1. Go to https://console.cloud.google.com/
2. Create a new project (or use an existing one)
3. Enable the **Custom Search API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Custom Search API"
   - Click "Enable"
4. Get an API Key:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy this key
   - (Recommended) Restrict the key to only the Custom Search API

#### Step 2: Create a Custom Search Engine
1. Go to https://programmablesearchengine.google.com/
2. Click "Add" to create a new search engine
3. In "Sites to search": enter `fanedit.org/*`
4. Name it (e.g., "Fanedit IFDB Search")
5. Click "Create"
6. Copy the **Search Engine ID** (usually a long alphanumeric string)

#### API Usage Limits
- Google Custom Search API has a free tier limit of **100 queries per day**
- If you need more, you may need to enable billing on your Google Cloud project

## Requirements
- Kodi 17+ (Krypton or later)
- Internet connection
- Google Custom Search API credentials (see Configuration section)

## Troubleshooting

If you experience issues:

1. **Settings page is blank**: Make sure you're using Kodi 17 or later. See [TESTING.md](TESTING.md) for detailed troubleshooting.
2. **Connection errors**: Verify your API credentials are correct and you haven't exceeded the 100 queries/day limit.
3. **No search results**: Check that your Custom Search Engine is configured for `fanedit.org/*` only.

For detailed testing and troubleshooting instructions, see [TESTING.md](TESTING.md).

## Notes
- If fanedit.org decides to block scraping or the format changes, this scraper will stop working
- API credentials are required for the scraper to function
