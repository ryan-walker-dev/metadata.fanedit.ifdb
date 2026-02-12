# Settings Page Fix Guide

## Problem
You may be seeing errors like:
```
error <CSettingGroup>: unknown setting type "text" of "api_key"
error <CSettingGroup>: unable to create new setting "api_key"
error <CSettingGroup>: unknown setting type "text" of "search_engine_id"
error <CSettingGroup>: unable to create new setting "search_engine_id"
```

And the settings page appears empty or only shows two text fields without labels.

## Root Cause
This was a bug in version 2.0.2 where the settings used `type="text"` which Kodi 21 doesn't recognize. Version 2.0.3 fixes this by using the correct `type="string"` format.

## Solution

### Step 1: Update to Version 2.0.3
Make sure you have the latest version:
1. Check your addon version in Kodi
2. Update to version 2.0.3 if you haven't already
3. You can verify the version in Kodi: **Settings → Add-ons → My Add-ons → Information Providers → IFDB**

### Step 2: Clear Kodi's Cache
Kodi caches settings definitions, so even after updating, you may see old errors:

**Option A: Restart Kodi** (recommended first step)
1. Completely exit and restart Kodi (not just reload skin)
2. This clears most caches

**Option B: Reinstall the addon** (if restart doesn't work)
1. Uninstall the IFDB addon
2. Restart Kodi
3. Reinstall the IFDB addon
4. Your settings may be preserved, but reconfigure if needed

**Option C: Clear addon data** (nuclear option)
1. Uninstall the IFDB addon
2. Manually delete the addon data folder:
   - **Windows**: `%APPDATA%\Kodi\userdata\addon_data\metadata.fanedit.ifdb`
   - **Linux**: `~/.kodi/userdata/addon_data/metadata.fanedit.ifdb`
   - **macOS**: `~/Library/Application Support/Kodi/userdata/addon_data/metadata.fanedit.ifdb`
3. Reinstall the IFDB addon
4. Reconfigure your API credentials

### Step 3: Verify the Fix
After updating and restarting:
1. Go to your movie library settings
2. Click on **Settings** for the IFDB scraper
3. You should now see:
   - **API Settings** header
   - **Google Custom Search Configuration** section
   - **Google API Key** field with label and help text
   - **Custom Search Engine ID** field with label and help text

## Verification Script

You can verify your installation is correct by running:
```bash
cd /path/to/addon
python3 validate_settings.py
```

This will check:
- ✓ Settings.xml is valid XML
- ✓ Structure matches Kodi 21 requirements
- ✓ All language strings are defined
- ✓ Settings use correct `type="string"` format
- ✓ All nested elements are present

Expected output:
```
✅ ALL CHECKS PASSED!
Your settings.xml is properly formatted for Kodi 21 Omega.
```

## What Was Fixed

### Version 2.0.2 (Incorrect - DO NOT USE)
```xml
<setting id="api_key" type="text" label="30001" default=""/>
```
❌ Used `type="text"` - NOT recognized by Kodi 21
❌ Used flat attributes - Deprecated format

### Version 2.0.3 (Correct - Current)
```xml
<setting id="api_key" type="string" label="30001" help="30003">
    <level>0</level>
    <default></default>
    <constraints>
        <allowempty>true</allowempty>
    </constraints>
    <control type="edit" format="string">
        <heading>30001</heading>
    </control>
</setting>
```
✅ Uses `type="string"` - Recognized by Kodi 21
✅ Uses nested elements - Modern Kodi format
✅ Matches official Kodi scrapers (TheMovieDB, etc.)

## Still Having Issues?

If you've followed all steps and still have problems:

1. **Check Kodi version**: This addon requires Kodi 21 (Omega) or later
   - For older Kodi versions (19/20), use version 1.x of this addon

2. **Check Kodi logs**: Look for any new error messages
   - **Settings → System → Logging → Enable debug logging**
   - Check the log file for details

3. **Run validation**: Use the validation script to check for issues
   ```bash
   python3 validate_settings.py
   ```

4. **Report the issue**: If nothing works, please report:
   - Your Kodi version
   - The addon version you installed
   - Any error messages from Kodi logs
   - Output from `validate_settings.py`

## Technical Details

For developers and curious users:

**Kodi 21 Settings Format Requirements:**
- Must use `<settings version="1">` root element
- Hierarchy: `settings → section → category → group → setting`
- Text input settings must use `type="string"` (NOT `type="text"`)
- Must include nested child elements:
  - `<level>` - Settings level (0 = basic, 1 = standard, 2 = advanced, etc.)
  - `<default>` - Default value
  - `<control>` - UI control definition
  - `<constraints>` - Optional constraints (e.g., allowempty)
- Control for text input: `<control type="edit" format="string">`

**References:**
- Official TheMovieDB scraper: https://github.com/xbmc/metadata.themoviedb.org.python/blob/master/resources/settings.xml
- Kodi Wiki - Add-on Settings: https://kodi.wiki/view/Add-on_settings
- Kodi Wiki - Settings Conversion: https://kodi.wiki/view/Add-on_settings_conversion

---

**Version 2.0.3** - Settings page now displays correctly in Kodi 21.3 Omega
