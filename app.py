import os

from flask import Flask, render_template


app = Flask(__name__)


@app.template_filter('plural')
def plural(s, count=None):
    # Would be nice to use inflect here, but it has a bug with all-caps input.
    return s if count == 1 else s + 's'


def online():
    # Production code
    #with open('/var/www/online.txt') as fl:
    #    raw_players = fl.read().splitlines()[4:-2]
    # Testing code
    raw_players = ['KeeKee (GM)', 'Pihro (GM)      ', 'LOFBot   ', 'Pyndragon', 'Ozthokk']
    
    count = len(raw_players)
    
    gms = []
    devs = []
    bots = []
    players = []
    
    for player in raw_players:
        player = player.rstrip()
        gm = False
        if player.endswith('(GM)'):
            gm = True
            player = player[:-4]
        player = player.rstrip()
        
        if player.startswith('LOFBot'):
            bots.append(player)
        elif player in ('Pihro', 'Pyndragon'):
            devs.append(player)
        elif gm:
            gms.append(player)
        else:
            players.append(player)
    
    return dict(count=count, gms=gms, players=players, bots=bots, devs=devs)


def gallery():
    # Production code
    #return os.listdir('/var/www/static/gallery')
    # Testing code
    return ['LOF_banner_still_licensed_web_4.png']


class Nav(object):
    registry = []
    
    def __init__(self, title, ref=None, url=None, external=False):
        self.title = title
        self.ref = ref if ref is not None else title.lower()
        self.url = url if url is not None else '/' + self.ref
        self.external = external
        
        self.registry.append(self)


def add_simple(*args, **kw):
    need_online = kw.pop('online', True)
    need_gallery = kw.pop('gallery', False)
    nav = Nav(*args, **kw)
    
    def func(ref=nav.ref, pages=nav.registry):
        kw = {'current': ref, 'pages': pages}
        if need_online:
            kw['online'] = online()
        if need_gallery:
            kw['gallery'] = gallery()
        
        return render_template(ref + '.html', **kw)
    
    app.add_url_rule(nav.url, nav.ref, func)


add_simple('Home', 'index', '/')
Nav('Forums', url='http://forums.landoffire.org', external=True)
Nav('Wiki', url='http://wiki.landoffire.org', external=True)
add_simple('Gallery', online=False, gallery=True)
add_simple('IRC')
add_simple('Project')
add_simple('Team')
add_simple('Donate')


if __name__ == '__main__':
    app.run(debug=True)