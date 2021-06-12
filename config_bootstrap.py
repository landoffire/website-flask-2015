import sys


DEBUG = '--debug' in sys.argv
ONLINE_LIST_PATH = './static/online.txt'
NEWS_PATH = './static/news.txt'
GALLERY_DIR = './static/gallery'

DISCORD_URL ='https://discord.gg/AHsEpZB'
FORUM_URL = 'http://forum.landoffire.org'

F_NORMAL = '0'
F_TITLE = '1'
F_AUTHOR = '3'
F_LIST = '9'

try:
    from config import *
except ImportError:
    pass
