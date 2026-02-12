#!/usr/bin/env python3
"""
Test script to validate the Python scraper structure
"""

import ast
import sys

def test_python_scraper():
    """Test that ifdb.py is valid and has required functions"""
    
    print("=" * 70)
    print("IFDB Python Scraper - Structure Validation")
    print("=" * 70)
    print()
    
    # Parse the Python file
    try:
        with open('ifdb.py', 'r') as f:
            code = f.read()
        
        tree = ast.parse(code)
        print("✓ Python syntax is valid")
        print()
    except SyntaxError as e:
        print(f"✗ Syntax error in ifdb.py: {e}")
        return False
    except FileNotFoundError:
        print("✗ File not found: ifdb.py")
        return False
    
    # Check for required functions
    required_functions = ['log', 'get_params', 'search_movie', 'get_details', 'main']
    found_functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            found_functions.append(node.name)
    
    print("Functions found:")
    for func in found_functions:
        print(f"  - {func}")
    print()
    
    missing_functions = [f for f in required_functions if f not in found_functions]
    if missing_functions:
        print(f"✗ Missing required functions: {', '.join(missing_functions)}")
        return False
    
    print("✓ All required functions present")
    print()
    
    # Check for required imports (accounting for submodule imports)
    required_base_imports = ['json', 're', 'sys', 'xbmc', 'xbmcaddon', 'xbmcgui', 'xbmcplugin']
    found_base_imports = []
    has_urllib = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found_base_imports.append(alias.name)
                if alias.name.startswith('urllib'):
                    has_urllib = True
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module_base = node.module.split('.')[0]
                found_base_imports.append(module_base)
                if module_base == 'urllib':
                    has_urllib = True
    
    print("Imports found:")
    for imp in set(found_base_imports):
        print(f"  - {imp}")
    if has_urllib:
        print("  - urllib (via submodules)")
    print()
    
    missing_imports = [i for i in required_base_imports if i not in found_base_imports]
    if missing_imports:
        print(f"✗ Missing required imports: {', '.join(missing_imports)}")
        return False
    
    if not has_urllib:
        print("✗ Missing urllib imports")
        return False
    
    print("✓ All required imports present")
    print()
    
    # Check for main guard
    has_main_guard = False
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            if hasattr(node.test, 'left') and hasattr(node.test.left, 'id'):
                if node.test.left.id == '__name__':
                    if hasattr(node.test, 'comparators'):
                        for comp in node.test.comparators:
                            if isinstance(comp, ast.Constant) and comp.value == '__main__':
                                has_main_guard = True
    
    if not has_main_guard:
        print("✗ Missing if __name__ == '__main__': guard")
        return False
    
    print("✓ Has proper main guard")
    print()
    
    return True

def main():
    """Main function"""
    success = test_python_scraper()
    
    print("=" * 70)
    if success:
        print("✓ TEST PASSED: Python scraper structure is valid")
    else:
        print("✗ TEST FAILED: Python scraper needs corrections")
    print("=" * 70)
    print()
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
