#!/usr/bin/env python

import json
import os
import sys
import warnings

USAGE = """
Usage: hosts.py --list
   Or: hosts.py --host <hostname>
""".strip()

def host_vars(guid, name):
    return {
        "ansible_host": '.'.join([name, guid, 'internal'])
    }

def get_all_hosts(guid):
    return {
        "apps": {
            "hosts": ["app1", "app2"]
        },
        "appdbs": {
            "hosts": ["appdb1"]
        },
        "frontends": {
            "hosts": ["frontend1"]
        },
        "internal": {
            "children": ["apps", "appdbs", "frontends"]
        },
        "_meta": {
            "hostvars": {
                "app1": host_vars(guid, 'app1'),
                "app2": host_vars(guid, 'app2'),
                "appdb1": host_vars(guid, 'appdb1'),
                "frontend1": host_vars(guid, 'frontend1')
            }
        }
    }

def die(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)

def main():
    guid = os.environ.get('GUID')
    if not guid:
        die("Dynamic inventory requires GUID environment variable.")
    if len(sys.argv) == 2 \
    and sys.argv[1] == '--list':
        print(json.dumps(
            get_all_hosts(guid),
            sort_keys=True,
            indent=2
        ))
    elif len(sys.argv) == 3 \
    and sys.argv[1] == '--host':
        print(json.dumps(
            host_vars(guid, sys.argv[2]),
            sort_keys=True,
            indent=2
        ))
    else:
        die(USAGE)

if __name__ == '__main__':
    main()
