import re
import os

import CommonMark as commonmark
from flask import Blueprint, Markup, abort, render_template, url_for

from nav import Nav


wiki_bp = Blueprint('wiki', __name__, static_folder='wiki_files')


TITLE_RE = re.compile('<h1>(.*)</h1>', re.DOTALL)


def _get_md(path):
    return os.path.extsep.join([path, 'md'])


def fn2title(filename):
    return os.path.basename(filename).replace('_', ' ').title()


def subordinate_headings(html):
    """
    Step all headings in the given html down in order to subordinate a embedded
    document.

    That is, convert h1's to h2's, h2's to h3's, and so on.
    """
    for i in range(5, 0, -1):
        s = i + 1
        html = html.replace('<h%s>' % i, '<h%s>' % s).replace('</h%s>' % i, '</h%s>' % s)
    return html


def read_wiki_page(path):
    # Turn the URL-style path into the canonical filesystem-aware path
    path = path.replace('/', os.path.sep).lower()

    full_path = os.path.join(wiki_bp.root_path, wiki_bp.static_folder, path)

    reg_path = _get_md(full_path)
    dir_path = _get_md(os.path.join(full_path, '_index'))

    if os.path.isfile(reg_path):
        full_path = reg_path
    elif os.path.isfile(dir_path):
        full_path = dir_path
    elif os.path.isdir(full_path):
        files = os.listdir(full_path)

        tmpl = '<h1>{}</h1>\n{}'
        title = fn2title(path) or 'Home'

        lines = []
        for f in files:
            if f.startswith('.'):
                continue

            f = os.path.splitext(f)[0]

            wiki_path = '/'.join([path, f]) if path else f
            if os.path.isdir(os.path.join(full_path, f)):
                wiki_path += '/'

            lines.append('<a href="{}">{}</a>'.format(url_for('.wiki', wiki_path=wiki_path), fn2title(f)))

        return tmpl.format(title, '<br>\n'.join(lines))
    else:
        abort(404)

    with open(full_path) as fl:
        return commonmark.commonmark(fl.read().decode('utf-8'))


@wiki_bp.route('/')
@wiki_bp.route('/<path:wiki_path>')
def wiki(wiki_path=''):
    wiki_path = wiki_path.strip('/')

    page = read_wiki_page(wiki_path)

    title_match = TITLE_RE.search(page)
    title = title_match.group(1) if title_match else None

    markup = Markup(subordinate_headings(page))

    nav = [['Home', '']]
    rebuilt = []
    for level in (wiki_path.split('/') if wiki_path else []):
        rebuilt.append(level)
        nav.append([fn2title(level), '/'.join(rebuilt) + '/'])

    title_from_path = nav.pop()[0]
    if not title:
        title = title_from_path

    return render_template('wiki.html', wiki_title=title, nav=nav, markup=markup,
                           current='wiki.wiki', pages=Nav.registry)
