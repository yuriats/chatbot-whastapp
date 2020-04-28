#!C:\Users\Yuri\Documents\chatbot\ananda\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'tqdm==4.40.2','console_scripts','tqdm'
__requires__ = 'tqdm==4.40.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('tqdm==4.40.2', 'console_scripts', 'tqdm')()
    )
