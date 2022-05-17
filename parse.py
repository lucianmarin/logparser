import gzip
from collections import defaultdict
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from jinja2 import DictLoader, Environment
from tqdm import tqdm
from user_agents import parse as uaparse

from template import TEMPLATE


def generate_html(days, browsers, systems, refs, hide, html):
    print('Generating HTML...', html)
    env = Environment(loader=DictLoader({'template.html': TEMPLATE}))
    template = env.get_template('template.html')
    with open(html, 'w') as file:
        output = template.render(
            days=sorted(days.items()),
            browsers=sorted(browsers.items(), key=lambda item: len(item[1])),
            systems=sorted(systems.items(), key=lambda item: len(item[1])),
            refs=sorted(refs.items(), key=lambda item: len(item[1])),
            hide=hide
        )
        file.write(output)


def console_print(days, browsers, systems, refs, hide):
    def display(key, value):
        if len(value) > hide:
            print(str(len(value)).rjust(tabs), key)
    dicts = [days, browsers, systems, refs]
    tabs = len(str(max(len(v) for d in dicts for v in d.values())))
    padding = "-" * tabs
    print(padding, 'Days')
    for key, value in sorted(days.items()):
        display(key, value)
    print()
    print(padding, 'Browsers')
    for key, value in sorted(browsers.items(), key=lambda item: len(item[1])):
        display(key, value)
    print()
    print(padding, 'Operating Systems')
    for key, value in sorted(systems.items(), key=lambda item: len(item[1])):
        display(key, value)
    print()
    print(padding, 'Referrers')
    for key, value in sorted(refs.items(), key=lambda item: len(item[1])):
        display(key, value)


def parse(gz_path, hide=0, html="", ignore=""):
    days = defaultdict(set)
    browsers = defaultdict(set)
    systems = defaultdict(set)
    refs = defaultdict(set)
    ignores = {r for r in ignore.split(',') if r}
    with gzip.open(gz_path, 'rt') as file:
        for line in tqdm(file, unit=""):
            log = CLFParser.logDict(line)
            ip = log['h']
            day = log['time'].strftime('%Y-%m-%d %A')
            days[day].add(ip)
            agent = uaparse(log["Useragent"][1:-1])
            if not agent.is_bot:
                browsers[agent.browser.family].add(ip)
                systems[agent.os.family].add(ip)
            a = urlparse(log["Referer"][1:-1].lower())
            netloc = a.netloc[4:] if a.netloc.startswith('www.') else a.netloc
            if netloc not in ignores:
                path = a.path[:-1]if a.path.endswith('/') else a.path
                refs[netloc + path].add(ip)
    if html:
        generate_html(days, browsers, systems, refs, hide, html)
    else:
        console_print(days, browsers, systems, refs, hide)


if __name__ == "__main__":
    Fire(parse)
