#!/usr/bin/env python3
"""
Test script to validate settings.xml format for Kodi 21 compatibility
"""

import xml.etree.ElementTree as ET
import sys

def test_settings_format(settings_file='resources/settings.xml'):
    """Test that settings.xml follows Kodi 21 format requirements"""
    
    print("=" * 70)
    print("IFDB Scraper - Settings Format Validation")
    print("=" * 70)
    print()
    
    try:
        # Parse the XML file
        tree = ET.parse(settings_file)
        root = tree.getroot()
        
        print(f"✓ Successfully parsed {settings_file}")
        print()
        
        # Check 1: Root element should be 'settings'
        if root.tag != 'settings':
            print(f"✗ Root element should be 'settings', found '{root.tag}'")
            return False
        print("✓ Root element is 'settings'")
        
        # Check 2: Root should have version="1" attribute
        version = root.get('version')
        if version != '1':
            print(f"✗ Settings should have version=\"1\", found version=\"{version}\"")
            return False
        print("✓ Settings has version=\"1\" attribute")
        
        # Check 3: Should have exactly one <section> element
        sections = root.findall('section')
        if len(sections) != 1:
            print(f"✗ Settings should have exactly 1 <section>, found {len(sections)}")
            return False
        print("✓ Settings has exactly 1 <section>")
        
        section = sections[0]
        section_id = section.get('id')
        if not section_id:
            print("✗ <section> should have an 'id' attribute")
            return False
        print(f"✓ Section has id=\"{section_id}\"")
        
        # Check 4: Section should have at least one <category>
        categories = section.findall('category')
        if len(categories) < 1:
            print("✗ Section should have at least 1 <category>")
            return False
        print(f"✓ Section has {len(categories)} category/categories")
        
        # Check 5: Each category should have at least one <group>
        for i, category in enumerate(categories):
            category_id = category.get('id')
            category_label = category.get('label')
            print(f"  Category {i+1}: id=\"{category_id}\", label=\"{category_label}\"")
            
            groups = category.findall('group')
            if len(groups) < 1:
                print(f"  ✗ Category '{category_id}' should have at least 1 <group>")
                return False
            print(f"    ✓ Has {len(groups)} group(s)")
            
            # Check 6: Each group should have at least one <setting>
            for j, group in enumerate(groups):
                group_id = group.get('id')
                settings = group.findall('setting')
                if len(settings) < 1:
                    print(f"    ✗ Group '{group_id}' should have at least 1 <setting>")
                    return False
                print(f"      Group {j+1} (id=\"{group_id}\"): {len(settings)} setting(s)")
                
                # Check each setting
                for setting in settings:
                    setting_id = setting.get('id')
                    setting_type = setting.get('type')
                    setting_label = setting.get('label')
                    print(f"        - {setting_id}: type=\"{setting_type}\", label=\"{setting_label}\"")
        
        print()
        print("✓ All format requirements met!")
        return True
        
    except ET.ParseError as e:
        print(f"✗ XML Parse Error: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ File not found: {settings_file}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {type(e).__name__}: {e}")
        return False

def main():
    """Main function"""
    print()
    
    settings_file = 'resources/settings.xml'
    if len(sys.argv) >= 2:
        settings_file = sys.argv[1]
    
    success = test_settings_format(settings_file)
    
    print()
    print("=" * 70)
    if success:
        print("✓ TEST PASSED: settings.xml format is compatible with Kodi 21")
    else:
        print("✗ TEST FAILED: settings.xml format needs correction")
    print("=" * 70)
    print()
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
