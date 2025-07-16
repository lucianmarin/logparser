import gzip
from collections import defaultdict
from functools import lru_cache
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from jinja2 import DictLoader, Environment
from tldextract import extract
from tqdm import tqdm
from user_agents import parse as uaparse

from template import TEMPLATE

BOTS = [
    "Amazonbot", "Applebot", "Bytespider", "FacebookBot", "Twitterbot",
    "FriendlyCrawler", "ISSCyberRiskCrawler", "YisouSpider",
    "Go-http-client", "http.rb", "scalaj-http",
    "Python aiohttp", "Python Requests",
]


@lru_cache(maxsize=None)
def get_hostname(value):
    r = extract(value)
    if not r.suffix:
        return r.domain
    if r.subdomain in ['', 'www']:
        return ".".join((r.domain, r.suffix))
    return ".".join((r.subdomain, r.domain, r.suffix))


@lru_cache(maxsize=None)
def get_link(value):
    a = urlparse(value)
    netloc = a.netloc[4:] if a.netloc.startswith('www.') else a.netloc
    path = a.path[:-1] if a.path.endswith('/') else a.path
    return netloc + path


def generate_file(days, browsers, systems, bots, refs, hide, file):
    print('Generating file...', file)
    env = Environment(loader=DictLoader({'template.html': TEMPLATE}))
    template = env.get_template('template.html')
    with open(file, 'w') as f:
        output = template.render(
            days=sorted(days.items()),
            browsers=sorted(browsers.items(), key=lambda item: len(item[1])),
            systems=sorted(systems.items(), key=lambda item: len(item[1])),
            bots=sorted(bots.items(), key=lambda item: len(item[1])),
            refs=sorted(refs.items(), key=lambda item: len(item[1])),
            hide=hide
        )
        f.write(output)


def console_print(days, browsers, systems, bots, refs, hide):
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
    print(padding, 'Bots')
    for key, value in sorted(bots.items(), key=lambda item: len(item[1])):
        display(key, value)
    print()
    print(padding, 'Referrers')
    for key, value in sorted(refs.items(), key=lambda item: len(item[1])):
        display(key, value)


def parse(path, hide=0, file="", skip=""):
    """
    Parse a gzipped log file.

    Args:
        path (str): Path to a gzipped log file
        hide (int): Hide rows with hide number of items
        file (str): Specify a .page file path
        skip (str): List referers to skip
    """
    days = defaultdict(set)
    browsers = defaultdict(set)
    systems = defaultdict(set)
    refs = defaultdict(set)
    bots = defaultdict(set)
    skipped = [i for i in skip.split(',') if i]
    with gzip.open(path, 'rt') as f:
        for line in tqdm(f, unit="l"):
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
    if page:
        generate_file(days, browsers, systems, bots, refs, hide, file)
    else:
        console_print(days, browsers, systems, bots, refs, hide)


if __name__ == "__main__":
    Fire(parse)
