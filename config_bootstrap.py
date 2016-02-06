import sys


DEBUG = '--debug' in sys.argv
ONLINE_LIST_PATH = '/var/www/online.txt'
NEWS_PATH = '/var/www/updates/news.txt'
GALLERY_DIR = '/var/www/static/gallery'

WIKI_URL ='http://wiki.landoffire.org'
FORUM_URL = 'http://forum.landoffire.org'

F_NORMAL = '0'
F_TITLE = '1'
F_AUTHOR = '3'
F_LIST = '9'


try:
    from config import *
except ImportError:
    pass
