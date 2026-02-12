# Testing Guide for IFDB Scraper v1.2.2

This guide will help you verify that the IFDB scraper is working correctly after the fixes.

## What Was Fixed

### Version 1.2.2 Changes:
1. **Settings page format fixed** - Updated from old format to compatible format that works with Kodi 17+
2. **Proper strings.po header added** - Added required gettext header for proper localization
3. **BOM removed from ifdb.xml** - Removed Byte Order Mark that could cause XML parsing issues
4. **Settings type corrected** - Changed from "string" to "text" for proper input fields

## Step-by-Step Testing Instructions

### Step 1: Install/Update the Addon

1. Remove the old version if installed:
   - Go to **Settings** → **Add-ons** → **My add-ons**
   - Find **IFDB** scraper
   - Click **Uninstall**

2. Install the new version:
   - Copy the entire `metadata.fanedit.ifdb` folder to your Kodi addons directory
   - Or create a ZIP file and install from ZIP
   - Restart Kodi

### Step 2: Verify Settings Page Displays Correctly

1. Go to **Settings** → **Media** → **Library**
2. Select a movie folder and click **Set content**
3. Choose **IFDB** as the scraper
4. Click **Settings** button for the IFDB scraper

**Expected Result:**
- Settings dialog should open (not blank)
- You should see two text input fields:
  - "Google API Key"
  - "Custom Search Engine ID"

**If settings page is still blank:**
- Check Kodi version (should be 17 or higher)
- Check Kodi log file for errors (see Troubleshooting section below)

### Step 3: Configure API Credentials

You need Google Custom Search API credentials. If you don't have them yet:

1. **Get Google API Key:**
   - Go to https://console.cloud.google.com/
   - Create a new project or use existing
   - Enable "Custom Search API"
   - Create an API Key under "Credentials"
   - Copy the key (starts with "AIzaSy...")

2. **Get Custom Search Engine ID:**
   - Go to https://programmablesearchengine.google.com/
   - Click "Add" to create new search engine
   - In "Sites to search": enter `fanedit.org/*`
   - Click "Create"
   - Copy the Search Engine ID (format: xxxxxxxxxxxxxxxxx)

3. **Enter in Kodi:**
   - Paste API Key in "Google API Key" field
   - Paste Search Engine ID in "Custom Search Engine ID" field
   - Click OK to save

### Step 4: Test Search Functionality

1. In your movie library, right-click on a folder
2. Choose **Scan for new content**
3. Or manually search for a specific movie:
   - Right-click on a movie
   - Choose **Change content**
   - Type a fanedit name (e.g., "The Empire Strikes Back Revisited")

**Expected Result:**
- Should show "Searching..." and then display search results
- Results should be from fanedit.org

**If you get "Unable to connect to remote server":**
- Verify your API credentials are correct
- Check your internet connection
- Use the test script (see below) to diagnose

### Step 5: Test Metadata Retrieval

1. Select a search result from fanedit.org
2. Wait for metadata to load

**Expected Result:**
- Movie title should appear
- Plot/synopsis should load
- Poster image should appear
- Additional metadata (genre, faneditor, year) should populate

## Using the Test Script

If you're having connection issues, you can test the API connection directly:

```bash
python3 test_api_connection.py YOUR_API_KEY YOUR_SEARCH_ENGINE_ID "The Empire Strikes Back"
```

The script will:
- Test the Google Custom Search API connection
- Show the constructed URL
- Display search results
- Verify fanedit.org results are returned

## Troubleshooting

### Settings Page is Blank

**Possible Causes:**
1. Kodi version too old (need 17+)
2. Language file not found
3. Corrupted installation

**Solutions:**
- Check Kodi version: **Settings** → **System** → **System Information**
- Verify all files are present, especially:
  - `resources/settings.xml`
  - `resources/language/resource.language.en_gb/strings.po`
- Try clean reinstall (uninstall, delete folder, reinstall)

### Connection Errors

**Error: "Unable to connect to remote server"**

**Possible Causes:**
1. API credentials not configured
2. Invalid API credentials
3. API quota exceeded (free tier: 100 queries/day)
4. Network/firewall blocking googleapis.com

**Solutions:**
- Verify credentials in settings
- Test credentials with test script
- Check Google Cloud Console for API usage/errors
- Check Kodi log for specific error messages

### No Search Results

**Possible Causes:**
1. Custom Search Engine not configured for fanedit.org
2. Search query doesn't match any fanedits
3. API returning results from wrong domain

**Solutions:**
- Verify Custom Search Engine is set to search only `fanedit.org/*`
- Try different search terms
- Use test script to see actual API response

### Metadata Not Loading

**Possible Causes:**
1. fanedit.org HTML structure changed
2. Cloudflare blocking requests
3. Network issues

**Solutions:**
- Try accessing the fanedit.org page directly in a browser
- Check if site is online
- Wait and retry later

## Checking Kodi Logs

To see detailed error messages:

1. Enable debug logging:
   - **Settings** → **System** → **Logging**
   - Enable **Enable debug logging**

2. View log location:
   - Windows: `%APPDATA%\Kodi\kodi.log`
   - Linux: `~/.kodi/temp/kodi.log`
   - macOS: `~/Library/Logs/kodi.log`

3. Look for lines containing:
   - "metadata.fanedit.ifdb"
   - "IFDB"
   - "CustomSearch"
   - "googleapis.com"

## API Quota Management

The free tier of Google Custom Search API allows **100 queries per day**.

**Tips to stay within quota:**
- Don't scan your entire library repeatedly
- Search for specific movies manually when possible
- If you need more, enable billing in Google Cloud Console

## Reporting Issues

If problems persist after following this guide, please report with:

1. Kodi version
2. Operating system
3. Error message (exact text)
4. Relevant lines from kodi.log
5. Whether settings page displays correctly
6. Whether test script works

## Success Indicators

✅ Settings page opens and shows two input fields
✅ Can enter and save API credentials
✅ Search returns results from fanedit.org
✅ Metadata loads correctly (title, plot, poster, etc.)
✅ No error messages in Kodi log

If all indicators pass, the scraper is working correctly!
