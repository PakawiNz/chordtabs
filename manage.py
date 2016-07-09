#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chordtabs.settings")

    from django.core.management import execute_from_command_line

    if len(sys.argv) == 2 and sys.argv[1] == 'extract':
        from viewer.utils import extract_link
        extract_link()
    elif len(sys.argv) == 2 and sys.argv[1] == 'download':
        from viewer.utils import download_all
    	download_all()
    else :
	    execute_from_command_line(sys.argv)
