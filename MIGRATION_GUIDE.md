# IFDB Scraper Version 2.0 - Migration Guide

## What Changed?

Version 2.0 represents a major architectural change from XML-based scraping to Python-based scraping.

### Why This Change Was Necessary

**Problem:** Settings page not showing in Kodi 21 (Omega)

**Root Cause:** Kodi 21 officially deprecated XML scrapers. While they still have limited support, the UI integration is incomplete, causing settings pages to not appear.

**Solution:** Complete conversion to Python scraper, which is the only officially supported scraper type for Kodi 21+.

## For Users

### What You Need to Know

1. **Kodi Version Requirements:**
   - Kodi 21 (Omega) or later: Use version 2.0.0+
   - Kodi 19/20 (Matrix/Nexus): Use version 1.x (XML scraper)

2. **Your Settings Are Preserved:**
   - Your API credentials will carry over automatically
   - No reconfiguration needed

3. **Same Functionality:**
   - Search and metadata extraction work the same way
   - Uses the same Google Custom Search API
   - Scrapes the same data from fanedit.org

### Installation

1. **Upgrading from 1.x to 2.0:**
   - Simply install the new version
   - Your settings will be preserved
   - Restart Kodi if settings don't appear immediately

2. **Fresh Installation:**
   - Install the addon from zip or repository
   - Configure your Google API credentials in Settings
   - Set IFDB as your movie scraper

## For Developers

### Technical Changes

1. **Main Scraper:**
   - Old: `ifdb.xml` (XML scraper)
   - New: `ifdb.py` (Python scraper)

2. **Dependencies:**
   - Added: `xbmc.python` version 3.0.0
   - Kept: `xbmc.metadata` version 2.1.0

3. **Python Implementation:**
   - Uses standard library only (urllib, json, re)
   - Follows Kodi Python scraper API conventions
   - Implements `find` and `getdetails` actions
   - Uses `InfoTagVideo` API for metadata

4. **Settings:**
   - Format unchanged (resources/settings.xml)
   - Read via `xbmcaddon.Addon().getSetting()`
   - Fully compatible with Kodi 21

### File Structure

```
metadata.fanedit.ifdb/
├── addon.xml                  # Updated with Python dependency
├── ifdb.py                    # NEW: Python scraper implementation
├── ifdb.xml                   # LEGACY: XML scraper (kept for reference)
├── resources/
│   ├── settings.xml          # Unchanged
│   └── language/
│       └── resource.language.en_gb/
│           └── strings.po    # Unchanged
├── test_python_scraper.py    # NEW: Validation test
├── test_settings_format.py   # Existing test
├── test_api_connection.py    # Existing test
└── .gitignore                # NEW: Exclude Python artifacts
```

### Testing

Run validation tests:

```bash
# Validate settings format
python3 test_settings_format.py

# Validate Python scraper structure
python3 test_python_scraper.py

# Test API connection (requires credentials)
python3 test_api_connection.py YOUR_API_KEY YOUR_SEARCH_ENGINE_ID
```

## Troubleshooting

### Settings Still Not Showing After Upgrade

1. Completely restart Kodi (not just reload skin)
2. Check that you're running Kodi 21 or later
3. Verify the addon version is 2.0.0 or higher
4. Check Kodi logs for any error messages

### Search Not Working

1. Verify your API credentials are still configured
2. Check you haven't exceeded the 100 queries/day limit
3. Test with `test_api_connection.py` script
4. Check Kodi logs for detailed error messages

## Support

- **GitHub Issues:** https://github.com/ryan-walker-dev/metadata.fanedit.ifdb/issues
- **Documentation:** See README.md and TESTING.md
- **Kodi Forum:** Search for IFDB scraper threads

## Credits

- Original XML scraper: TomFin46
- Python conversion: ryan-walker-dev with GitHub Copilot
- Google Custom Search API integration
