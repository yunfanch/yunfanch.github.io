"""Generate an accessible static Chinese edition from the shared English pages."""
import json
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class ChinesePage(HTMLParser):
    def __init__(self, page, translations, titles):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.translations = translations
        self.titles = titles
        self.out = []
        self.raw_depth = 0

    def handle_decl(self, decl):
        self.out.append('<!' + decl + '>')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.raw_depth += 1
        if tag == 'html':
            a['lang'] = 'zh-CN'
        for key in ('aria-label', 'alt', 'title', 'content'):
            if key in a:
                a[key] = self.translations.get(a[key], a[key])
        for key in ('href', 'src'):
            value = a.get(key, '')
            if value.startswith('assets/'):
                a[key] = '../' + value
            elif value.startswith('zh/'):
                a[key] = value[3:]
        if a.get('data-language') == 'en':
            a['href'] = '../' + self.page
            a.pop('aria-current', None)
        elif a.get('data-language') == 'zh':
            a['href'] = self.page
            a['aria-current'] = 'page'
        if tag == 'link' and a.get('rel') == 'canonical':
            a['href'] = 'https://yunfanch.github.io/zh/' + ('' if self.page == 'index.html' else self.page)
        if tag == 'meta' and a.get('property') == 'og:url':
            a['content'] = 'https://yunfanch.github.io/zh/' + ('' if self.page == 'index.html' else self.page)
        if tag == 'meta' and a.get('property') == 'og:locale':
            a['content'] = 'zh_CN'
        attributes = ''.join(' ' + k + ('' if v is None else '="' + escape(v, quote=True) + '"') for k, v in a.items())
        self.out.append('<' + tag + attributes + '>')

    def handle_endtag(self, tag):
        self.out.append('</' + tag + '>')
        if tag in ('script', 'style'):
            self.raw_depth -= 1

    def handle_data(self, data):
        if self.raw_depth:
            self.out.append(data)
            return
        key = data.strip()
        if not key:
            self.out.append(data)
            return
        translated = self.translations.get(key, key)
        leading = data[:len(data) - len(data.lstrip())]
        trailing = data[len(data.rstrip()):] if data.rstrip() != data else ''
        self.out.append(escape(leading + translated + trailing, quote=False))
        if key in self.titles and key != translated:
            self.out.append('<span class="original-title" lang="en">' + escape(key) + '</span>')


def build_chinese():
    translations = json.loads((ROOT / 'translations.zh.json').read_text())
    content = json.loads((ROOT / 'content.json').read_text())
    titles = {p['title'] for category in ('publications', 'manuscripts_under_review', 'manuscripts_in_preparation') for p in content[category]}
    (ROOT / 'zh').mkdir(exist_ok=True)
    for page in ('index.html', 'cv.html'):
        parser = ChinesePage(page, translations, titles)
        parser.feed((ROOT / page).read_text())
        (ROOT / 'zh' / page).write_text(''.join(parser.out))
