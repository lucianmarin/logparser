import gzip
from collections import defaultdict
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from jinja2 import DictLoader, Environment
from tqdm import tqdm
from user_agents import parse as uaparse

from template import TEMPLATE


def generate_html(days, browsers, systems, refs, html):
    print('Generating HTML...', html)
    env = Environment(loader=DictLoader({'template.html': TEMPLATE}))
    template = env.get_template('template.html')
    with open(html, 'w') as file:
        output = template.render(
            days=sorted(days.items()),
            browsers=sorted(browsers.items(), key=lambda item: len(item[1])),
            systems=sorted(systems.items(), key=lambda item: len(item[1])),
            refs=sorted(refs.items(), key=lambda item: len(item[1]))
        )
        file.write(output)


def console_print(days, browsers, systems, refs):
    dicts = [days, browsers, systems, refs]
    pad = len(str(max(len(v) for d in dicts for v in d.values())))
    print('-' * pad, 'Days')
    for k, v in sorted(days.items()):
        print(str(len(v)).rjust(pad), k)
    print()
    print('-' * pad, 'Browsers')
    for k, v in sorted(browsers.items(), key=lambda item: len(item[1])):
        print(str(len(v)).rjust(pad), k)
    print()
    print('-' * pad, 'Operating Systems')
    for k, v in sorted(systems.items(), key=lambda item: len(item[1])):
        print(str(len(v)).rjust(pad), k)
    print()
    print('-' * pad, 'Referrers')
    for k, v in sorted(refs.items(), key=lambda item: len(item[1])):
        print(str(len(v)).rjust(pad), k)


def parse(gz_path, html=None, skip_ref=""):
    days = defaultdict(set)
    browsers = defaultdict(set)
    systems = defaultdict(set)
    refs = defaultdict(set)
    skip_refs = [r for r in skip_ref.split(',') if r]
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
            path = a.path[:-1]if a.path.endswith('/') else a.path
            ref = "{0}{1}".format(netloc, path)
            if not any(s in ref for s in skip_refs):
                refs[ref].add(ip)
    if html:
        generate_html(days, browsers, systems, refs, html)
    else:
        console_print(days, browsers, systems, refs)


if __name__ == "__main__":
    Fire(parse)
