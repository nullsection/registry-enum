#!/usr/bin/env python3
"""
Windows Registry Scanner
Recursively scans registry keys and values for a specified search string.
Usage: python reg.py <search_string>
Example: python reg.py ".dll"
"""

import winreg
import sys
import argparse
from typing import List, Tuple


# Registry root keys to scan
ROOT_KEYS = {
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
}


def scan_registry_key(root_key, key_path: str, search_string: str, case_sensitive: bool = False) -> List[Tuple[str, str, str]]:
    """
    Recursively scan a registry key for the search string.

    Args:
        root_key: Registry root key handle
        key_path: Path to the registry key
        search_string: String to search for
        case_sensitive: Whether to perform case-sensitive search

    Returns:
        List of tuples (full_path, match_type, match_value)
    """
    results = []
    search_str = search_string if case_sensitive else search_string.lower()

    try:
        # Open the registry key
        key = winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ)

        # Check if the key name itself contains the search string
        key_name = key_path.split('\\')[-1] if '\\' in key_path else key_path
        check_name = key_name if case_sensitive else key_name.lower()
        if search_str in check_name:
            results.append((key_path, "KEY_NAME", key_name))

        # Enumerate and check all values in this key
        try:
            value_index = 0
            while True:
                try:
                    value_name, value_data, value_type = winreg.EnumValue(key, value_index)
                    value_index += 1

                    # Check value name
                    check_value_name = value_name if case_sensitive else value_name.lower()
                    if search_str in check_value_name:
                        results.append((key_path, "VALUE_NAME", value_name))

                    # Check value data (convert to string if possible)
                    if value_data is not None:
                        try:
                            value_str = str(value_data)
                            check_value_str = value_str if case_sensitive else value_str.lower()
                            if search_str in check_value_str:
                                results.append((key_path, "VALUE_DATA", f"{value_name} = {value_str}"))
                        except:
                            pass

                except OSError:
                    break
        except Exception as e:
            pass

        # Enumerate and recurse into subkeys
        try:
            subkey_index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, subkey_index)
                    subkey_index += 1

                    # Build full subkey path
                    if key_path:
                        subkey_path = f"{key_path}\\{subkey_name}"
                    else:
                        subkey_path = subkey_name

                    # Recursively scan the subkey
                    subkey_results = scan_registry_key(root_key, subkey_path, search_string, case_sensitive)
                    results.extend(subkey_results)

                except OSError:
                    break
        except Exception as e:
            pass

        winreg.CloseKey(key)

    except PermissionError:
        # Skip keys we don't have permission to access
        pass
    except FileNotFoundError:
        # Skip keys that don't exist
        pass
    except Exception as e:
        # Skip other errors silently
        pass

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Recursively scan Windows Registry for a search string",
        epilog="Example: python reg.py \".dll\""
    )
    parser.add_argument("search_string", help="String to search for in registry keys and values")
    parser.add_argument("-c", "--case-sensitive", action="store_true", help="Perform case-sensitive search")
    parser.add_argument("-r", "--root", choices=list(ROOT_KEYS.keys()),
                       help="Scan only a specific root key (default: all roots)")
    parser.add_argument("-o", "--output", help="Output results to a file")

    args = parser.parse_args()

    print(f"Scanning Windows Registry for: '{args.search_string}'")
    print(f"Case sensitive: {args.case_sensitive}")
    print("This may take a while...\n")

    all_results = []

    # Determine which root keys to scan
    roots_to_scan = {args.root: ROOT_KEYS[args.root]} if args.root else ROOT_KEYS

    for root_name, root_key in roots_to_scan.items():
        print(f"Scanning {root_name}...")
        results = scan_registry_key(root_key, "", args.search_string, args.case_sensitive)

        for full_path, match_type, match_value in results:
            result_line = f"[{root_name}\\{full_path}] {match_type}: {match_value}"
            all_results.append(result_line)
            print(result_line)

    print(f"\n{'='*80}")
    print(f"Scan complete. Found {len(all_results)} matches.")

    # Save to file if requested
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"Registry Scan Results for: '{args.search_string}'\n")
                f.write(f"Case sensitive: {args.case_sensitive}\n")
                f.write('='*80 + '\n\n')
                for result in all_results:
                    f.write(result + '\n')
            print(f"Results saved to: {args.output}")
        except Exception as e:
            print(f"Error saving to file: {e}")


if __name__ == "__main__":
    main()
