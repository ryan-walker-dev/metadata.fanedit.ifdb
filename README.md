# metadata.fanedit.ifdb
Kodi Movie Information Scraper for the Internet Fanedit Database using Google Custom Search API

**Current Version: 2.0.3** - Fixed settings page display issue in Kodi 21

Metadata agent for scraping information from the Internet Fanedit Database (IFDB) at https://fanedit.org/

## Recent Updates

### v2.0.3 (2026-02-12)
- ✅ **Fixed settings page display** - Settings now show correctly in Kodi 21.3
- ✅ Corrected setting type format (`type="string"` with nested elements)
- ✅ Matches official Kodi scraper standards (TheMovieDB format)
- ✅ Added comprehensive validation tools

### v2.0.0
- ✅ **Converted from XML to Python scraper** - Required for Kodi 21 Omega compatibility
- ✅ Settings page now works properly in Kodi 21+
- ✅ Full support for modern Kodi versions (21 Omega and later)
- ✅ Improved error handling and user feedback
- ✅ Uses Python 3 for better reliability and maintainability

See [CHANGELOG.md](CHANGELOG.md) for complete version history.
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
- Kodi 21+ (Omega or later) - **Required for Python scraper support**
  - Kodi 21 (Omega) - Fully supported
  - Kodi 19/20 (Matrix/Nexus) - Not supported (use XML scraper version 1.x)
- Internet connection
- Google Custom Search API credentials (see Configuration section)

## Troubleshooting

### Settings Page Issues

#### "Settings page is empty" or shows errors like "unknown setting type 'text'"

**Solution:**
1. **Ensure you're running version 2.0.3 or later** - Check in Kodi's addon information
2. **Completely restart Kodi** (not just reload skin) - Settings are cached
3. **Clear addon data** if restart doesn't work:
   - Uninstall the addon
   - Delete addon data folder (varies by platform)
   - Reinstall the addon
4. **Verify installation** - Run validation script:
   ```bash
   python3 validate_settings.py
   ```
   This will check if settings.xml is properly formatted

**Why this happens:**
- Versions before 2.0.3 had incorrect settings format
- Kodi caches settings definitions and may not reload them properly
- The error "unknown setting type 'text'" indicates an old cached version

**Current correct format** (v2.0.3):
- Uses `type="string"` (NOT `type="text"`)
- Uses nested XML elements (matches TheMovieDB scraper)
- All validation tests pass

If you experience other issues:

1. **Settings page is not showing at all (Kodi 21+)**: 
   - Update to version 2.0.0 or later, which uses a Python scraper required by Kodi 21
   - Older XML-based versions (1.x) are not fully compatible with Kodi 21
   
2. **Connection errors**: Verify your API credentials are correct and you haven't exceeded the 100 queries/day limit.

3. **No search results**: Check that your Custom Search Engine is configured for `fanedit.org/*` only.

For detailed testing and troubleshooting instructions, see [TESTING.md](TESTING.md).

## Notes
- Version 2.0.0 and later requires Kodi 21 (Omega) or newer
- For Kodi 19/20, use version 1.x (XML scraper)
- If fanedit.org decides to block scraping or the format changes, this scraper will stop working
- API credentials are required for the scraper to function
