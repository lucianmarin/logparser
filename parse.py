import gzip
from collections import defaultdict
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from jinja2 import DictLoader, Environment
from tqdm import tqdm
from user_agents import parse as uaparse
from tldextract import extract

from template import TEMPLATE

BOTS = [
    "Amazonbot", "Applebot", "Bytespider", "FacebookBot", "Twitterbot",
    "Go-http-client", "http.rb", "scalaj-http",
    "Python aiohttp", "Python Requests",
]


def get_hostname(value):
    r = extract(value)
    if not r.suffix:
        return r.domain
    if r.subdomain in ['', 'www']:
        return ".".join((r.domain, r.suffix))
    return ".".join((r.subdomain, r.domain, r.suffix))


def get_link(value):
    a = urlparse(value)
    netloc = a.netloc[4:] if a.netloc.startswith('www.') else a.netloc
    path = a.path[:-1] if a.path.endswith('/') else a.path
    return netloc + path


def generate_html(days, browsers, systems, bots, refs, lowest, html):
    print('Generating HTML...', html)
    env = Environment(loader=DictLoader({'template.html': TEMPLATE}))
    template = env.get_template('template.html')
    with open(html, 'w') as file:
        output = template.render(
            days=sorted(days.items()),
            browsers=sorted(browsers.items(), key=lambda item: len(item[1])),
            systems=sorted(systems.items(), key=lambda item: len(item[1])),
            bots=sorted(bots.items(), key=lambda item: len(item[1])),
            refs=sorted(refs.items(), key=lambda item: len(item[1])),
            lowest=lowest
        )
        file.write(output)


def console_print(days, browsers, systems, bots, refs, lowest):
    def display(key, value):
        if len(value) > lowest:
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
    print(padding, 'Bots')
    for key, value in sorted(bots.items(), key=lambda item: len(item[1])):
        display(key, value)
    print()
    print(padding, 'Referrers')
    for key, value in sorted(refs.items(), key=lambda item: len(item[1])):
        display(key, value)


def parse(gz_path, lowest=0, html="", skip=""):
    """
    Parse a gzipped log file.

    Args:
        gz_path (str): Path to a gzipped log file
        lowest (int): Hide rows with lowest number of items
        html (str): Specify a .html file path
        skip (str): List referers to skip
    """
    days = defaultdict(set)
    browsers = defaultdict(set)
    systems = defaultdict(set)
    refs = defaultdict(set)
    bots = defaultdict(set)
    skipped = [i for i in skip.split(',') if i]
    with gzip.open(gz_path, 'rt') as file:
        for line in tqdm(file, unit="l"):
            log = CLFParser.logDict(line)
            ip = log['h']
            agent = uaparse(log["Useragent"][1:-1])
            if agent.is_bot or agent.browser.family in BOTS:
                bots[agent.browser.family].add(ip)
            else:
                day = log['time'].strftime('%Y-%m-%d %A')
                days[day].add(ip)
                browsers[agent.browser.family].add(ip)
                systems[agent.os.family].add(ip)
                ref = log["Referer"][1:-1].lower()
                link = get_link(ref)
                hostname = get_hostname(ref)
                if hostname not in skipped:
                    refs[link].add(ip)
    if html:
        generate_html(days, browsers, systems, bots, refs, lowest, html)
    else:
        console_print(days, browsers, systems, bots, refs, lowest)


if __name__ == "__main__":
    Fire(parse)
