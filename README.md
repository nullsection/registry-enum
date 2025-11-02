# registry-enum

```
usage: reg.py [-h] [-c] [-r {HKEY_CLASSES_ROOT,HKEY_CURRENT_USER,HKEY_LOCAL_MACHINE,HKEY_USERS,HKEY_CURRENT_CONFIG}]
              [-o OUTPUT]
              search_string

Recursively scan Windows Registry for a search string

positional arguments:
  search_string         String to search for in registry keys and values

options:
  -h, --help            show this help message and exit
  -c, --case-sensitive  Perform case-sensitive search
  -r {HKEY_CLASSES_ROOT,HKEY_CURRENT_USER,HKEY_LOCAL_MACHINE,HKEY_USERS,HKEY_CURRENT_CONFIG}, --root {HKEY_CLASSES_ROOT,HKEY_CURRENT_USER,HKEY_LOCAL_MACHINE,HKEY_USERS,HKEY_CURRENT_CONFIG}
                        Scan only a specific root key (default: all roots)
  -o OUTPUT, --output OUTPUT
                        Output results to a file

Example: python reg.py "bitlocker"

```
