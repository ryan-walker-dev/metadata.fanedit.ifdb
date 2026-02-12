#!/usr/bin/env python3
"""
Comprehensive validation script for settings.xml and language strings.
This helps diagnose why settings might not display correctly in Kodi.
"""

import xml.etree.ElementTree as ET
import sys
import os

def validate_settings():
    """Validate settings.xml structure and references"""
    print("=" * 70)
    print("IFDB Scraper - Comprehensive Settings Validation")
    print("=" * 70)
    print()
    
    errors = []
    warnings = []
    
    # 1. Check settings.xml exists and is valid XML
    settings_path = 'resources/settings.xml'
    if not os.path.exists(settings_path):
        errors.append(f"Settings file not found: {settings_path}")
        return False, errors, warnings
    
    try:
        tree = ET.parse(settings_path)
        root = tree.getroot()
        print("✓ Settings.xml is valid XML")
    except ET.ParseError as e:
        errors.append(f"XML parse error: {e}")
        return False, errors, warnings
    
    # 2. Check root structure
    if root.tag != 'settings':
        errors.append(f"Root element should be 'settings', got '{root.tag}'")
    if root.get('version') != '1':
        errors.append(f"Settings version should be '1', got '{root.get('version')}'")
    
    if not errors:
        print("✓ Root element structure is correct")
    
    # 3. Check section/category/group hierarchy
    sections = root.findall('section')
    if len(sections) != 1:
        errors.append(f"Should have exactly 1 section, found {len(sections)}")
    else:
        section = sections[0]
        section_id = section.get('id')
        print(f"✓ Found section: id='{section_id}'")
        
        categories = section.findall('category')
        if not categories:
            errors.append("Section must contain at least one category")
        
        for cat in categories:
            cat_id = cat.get('id')
            cat_label = cat.get('label')
            print(f"✓ Category: id='{cat_id}', label='{cat_label}'")
            
            if not cat_label:
                warnings.append(f"Category '{cat_id}' has no label")
            
            groups = cat.findall('group')
            if not groups:
                errors.append(f"Category '{cat_id}' must contain at least one group")
            
            for group in groups:
                group_id = group.get('id')
                group_label = group.get('label')
                print(f"  ✓ Group: id='{group_id}', label='{group_label}'")
                
                if not group_label:
                    warnings.append(f"Group '{group_id}' has no label (may appear blank in UI)")
                
                settings = group.findall('setting')
                if not settings:
                    errors.append(f"Group '{group_id}' must contain at least one setting")
                
                # 4. Check each setting
                for setting in settings:
                    setting_id = setting.get('id')
                    setting_type = setting.get('type')
                    setting_label = setting.get('label')
                    setting_help = setting.get('help')
                    
                    print(f"    ✓ Setting: id='{setting_id}', type='{setting_type}', label='{setting_label}', help='{setting_help}'")
                    
                    # Validate setting type
                    if setting_type == 'text':
                        errors.append(f"Setting '{setting_id}' uses type='text' which is NOT valid in Kodi 21. Use type='string' instead.")
                    elif setting_type != 'string':
                        warnings.append(f"Setting '{setting_id}' uses type='{setting_type}' - verify this is correct")
                    
                    if not setting_label:
                        warnings.append(f"Setting '{setting_id}' has no label")
                    
                    # Check for required nested elements
                    level = setting.find('level')
                    default = setting.find('default')
                    control = setting.find('control')
                    
                    if level is None:
                        warnings.append(f"Setting '{setting_id}' missing <level> element (should be <level>0</level>)")
                    else:
                        print(f"      ✓ Has <level>{level.text}</level>")
                    
                    if default is None:
                        warnings.append(f"Setting '{setting_id}' missing <default> element")
                    else:
                        default_val = default.text if default.text else ""
                        print(f"      ✓ Has <default>{default_val}</default>")
                    
                    if control is None:
                        errors.append(f"Setting '{setting_id}' missing <control> element")
                    else:
                        control_type = control.get('type')
                        control_format = control.get('format')
                        print(f"      ✓ Has <control type='{control_type}' format='{control_format}'>")
                        
                        if setting_type == 'string' and control_type != 'edit':
                            warnings.append(f"Setting '{setting_id}' type='string' usually needs control type='edit'")
                        
                        heading = control.find('heading')
                        if heading is not None:
                            print(f"        ✓ Control has <heading>{heading.text}</heading>")
    
    # 5. Collect all label/help string references
    string_refs = set()
    for elem in root.iter():
        for attr in ['label', 'help']:
            val = elem.get(attr)
            if val:
                string_refs.add(val)
        # Also check heading elements
        if elem.tag == 'heading' and elem.text:
            string_refs.add(elem.text)
    
    print()
    print(f"Found {len(string_refs)} string references: {sorted(string_refs)}")
    
    # 6. Validate language strings exist
    strings_path = 'resources/language/resource.language.en_gb/strings.po'
    if not os.path.exists(strings_path):
        errors.append(f"Language file not found: {strings_path}")
    else:
        with open(strings_path, 'r', encoding='utf-8') as f:
            strings_content = f.read()
        
        print()
        print(f"Checking language strings in {strings_path}...")
        
        for string_ref in sorted(string_refs):
            if f'msgid "{string_ref}"' in strings_content:
                # Extract the msgstr
                try:
                    idx = strings_content.index(f'msgid "{string_ref}"')
                    snippet = strings_content[idx:idx+200]
                    msgstr_start = snippet.index('msgstr "') + 8
                    msgstr_end = snippet.index('"', msgstr_start)
                    msgstr_val = snippet[msgstr_start:msgstr_end]
                    print(f"  ✓ {string_ref}: \"{msgstr_val}\"")
                except:
                    print(f"  ✓ {string_ref}: (found but couldn't parse value)")
            else:
                errors.append(f"String '{string_ref}' referenced in settings.xml but not found in strings.po")
    
    # 7. Summary
    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if errors:
        print(f"\n❌ {len(errors)} ERROR(S) FOUND:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYour settings.xml is properly formatted for Kodi 21 Omega.")
        print("If settings still don't show correctly in Kodi:")
        print("  1. Completely restart Kodi (not just reload skin)")
        print("  2. Clear Kodi's cache/data directory")
        print("  3. Reinstall the addon")
        print("  4. Check Kodi logs for additional errors")
    elif not errors:
        print("\n✅ NO ERRORS (warnings are usually non-critical)")
    else:
        print("\n❌ VALIDATION FAILED")
        print("\nFix the errors above and re-run this script.")
    
    print("=" * 70)
    print()
    
    return len(errors) == 0, errors, warnings

if __name__ == '__main__':
    success, errors, warnings = validate_settings()
    sys.exit(0 if success else 1)
