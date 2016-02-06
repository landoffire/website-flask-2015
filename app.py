import os

from flask import Flask, render_template

import config_bootstrap as config


app = Flask(__name__)


@app.template_filter('plural')
def plural(s, count=None):
    # Would be nice to use inflect here, but it has a bug with all-caps input.
    return s if count == 1 else s + 's'


def online():
    if config.DEBUG:
        raw_players = ['KeeKee (GM)', 'Pihro (GM)      ', 'LOFBot   ', 'Pyndragon', 'Ozthokk']
    else:
        with open(config.ONLINE_LIST_PATH) as fl:
            raw_players = unicode(fl.read(), 'utf-8').splitlines()[4:-2]

    count = len(raw_players)

    gms = []
    devs = []
    bots = []
    players = []

    for player in sorted(raw_players):
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


def news():
    with open('news.txt' if config.DEBUG else config.NEWS_PATH) as fl:
        paragraphs = unicode(fl.read(), 'utf-8').split('\n\n')

    output = []
    lines_remaining = 25
    for p in paragraphs:
        if lines_remaining <= 0:
            break

        lines = [(L[2], L[4:]) for L in p.splitlines(True)]
        lines_remaining -= len(lines)

        ident = lines[0][0]
        if ident == config.F_LIST:
            parsed = ['list', lines[0][1], [L[1][2:] for L in lines[1:]]]
        elif ident == config.F_AUTHOR and lines[0][1].startswith(u'\u2014'):
            # Strip off leading em-dash and whitespace
            parsed = ['author', lines[0][1][1:].rstrip()]
        else:
            name = {config.F_NORMAL: 'normal', config.F_TITLE: 'title', config.F_AUTHOR: 'author'}.get(ident, 'normal')
            parsed = [name, '\n'.join(L[1] for L in lines)]

        output.append(parsed)

    return output


def gallery():
    if config.DEBUG:
        return ['LOF_banner_still_licensed_web_4.png']
    else:
        return os.listdir(config.GALLERY_DIR)


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
    need_news = kw.pop('news', True)
    need_gallery = kw.pop('gallery', False)
    nav = Nav(*args, **kw)

    def func(ref=nav.ref, pages=nav.registry):
        kw = {'current': ref, 'pages': pages}
        if need_news:
            kw['news'] = news()
        if need_online:
            kw['online'] = online()
        if need_gallery:
            kw['gallery'] = gallery()

        return render_template(ref + '.html', **kw)

    app.add_url_rule(nav.url, nav.ref, func)


add_simple('Home', 'index', '/')
Nav('Forum', url=config.FORUM_URL, external=True)
Nav('Wiki', url=config.WIKI_URL, external=True)
add_simple('Gallery', online=False, news=False, gallery=True)
add_simple('IRC')
add_simple('Project')
add_simple('Team')
add_simple('Donate')


if __name__ == '__main__':
    app.run(debug=config.DEBUG)
