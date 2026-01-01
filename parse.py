import gzip
import re
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from urllib.parse import urlparse

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

COMBINED_LOG_FORMAT = re.compile(r'(?P<h>([^ ]*)) (?P<l>([^ ]*)) (?P<u>([^ ]*)) (?P<t>\[([^]]*)\]) (?P<r>"([^"]*)") (?P<s>([^ ]*)) (?P<b>([^ ]*)) (?P<Referer>"([^"]*)") (?P<Useragent>"([^"]*)")')
COMMON_LOG_FORMAT = re.compile(r'(?P<h>([^ ]*)) (?P<l>([^ ]*)) (?P<u>([^ ]*)) (?P<t>\[([^]]*)\]) (?P<r>"([^"]*)") (?P<s>([^ ]*)) (?P<b>([^ ]*))')


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


@lru_cache(maxsize=None)
def get_ua(ua_string):
    return uaparse(ua_string)


@lru_cache(maxsize=None)
def get_day_from_str(date_str):
    # date_str format: 01/Jan/2022
    dt = datetime.strptime(date_str, '%d/%b/%Y')
    return dt.strftime('%Y-%m-%d %A')


def generate_html(days, browsers, systems, bots, refs, hide, html):
    print('Generating html...', html)
    env = Environment(loader=DictLoader({'template.html': TEMPLATE}))
    template = env.get_template('template.html')
    with open(html, 'w') as f:
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


def parse(gz_path, hide=0, html="", skip=""):
    """
    Parse a gzipped log file.

    Args:
        path (str): Path to a gzipped log file
        hide (int): Hide rows with hide number of items
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
            m = COMBINED_LOG_FORMAT.match(line)
            if m:
                log = m.groupdict()
            else:
                m = COMMON_LOG_FORMAT.match(line)
                if m:
                    log = m.groupdict()
                    log['Useragent'] = ""
                    log['Referer'] = ""
                else:
                    continue

            ip = log['h']
            agent = get_ua(log["Useragent"][1:-1])
            if agent.is_bot or agent.browser.family in BOTS:
                bots[agent.browser.family].add(ip)
            else:
                # log['t'] is like [01/Jan/2022:00:00:00 +0000]
                # we want 01/Jan/2022 which is index 1 to 12
                date_part = log['t'][1:12]
                day = get_day_from_str(date_part)
                days[day].add(ip)
                browsers[agent.browser.family].add(ip)
                systems[agent.os.family].add(ip)
                ref = log["Referer"][1:-1].lower()
                link = get_link(ref)
                hostname = get_hostname(ref)
                if hostname not in skipped:
                    refs[link].add(ip)
    if html:
        generate_html(days, browsers, systems, bots, refs, hide, html)
    else:
        console_print(days, browsers, systems, bots, refs, hide)


if __name__ == "__main__":
    Fire(parse)
