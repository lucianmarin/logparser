import gzip
from collections import defaultdict
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from jinja2 import Environment, DictLoader
from tqdm import tqdm
from user_agents import parse as uaparse

SKIP_REFS = ["subreply.com", "unfeeder.com"]


def generate_html(days, browsers, oses, refs, html):
    print('Generating HTML...', html)
    with open(html) as file:
        template = file.read()
    env = Environment(loader=DictLoader({'template.html': template}))
    template = env.get_template('template.html')
    with open(html, 'w') as file:
        output = template.render(
            days=sorted(days.items()),
            oses=sorted(oses.items(), key=lambda item: len(item[1])),
            browsers=sorted(browsers.items(), key=lambda item: len(item[1])),
            refs=sorted(refs.items(), key=lambda item: len(item[1]))
        )
        file.write(output)


def console_print(days, browsers, oses, refs):
    print('----- Day')
    for k, v in sorted(days.items()):
        print(str(len(v)).rjust(5), k)
    print('\n----- OS')
    for k, v in sorted(oses.items(), key=lambda item: len(item[1])):
        print(str(len(v)).rjust(5), k)
    print('\n----- Browser')
    for k, v in sorted(browsers.items(), key=lambda item: len(item[1])):
        print(str(len(v)).rjust(5), k)
    print('\n----- Referer')
    for k, v in sorted(refs.items(), key=lambda item: len(item[1])):
        print(str(len(v)).rjust(5), k)


def parse(gz_path, html=None):
    days = defaultdict(set)
    browsers = defaultdict(set)
    oses = defaultdict(set)
    refs = defaultdict(set)
    with gzip.open(gz_path, 'rt') as file:
        for line in tqdm(file, unit=""):
            log = CLFParser.logDict(line)
            ip = log['h']
            day = log['time'].strftime('%Y-%m-%d %a')
            days[day].add(ip)
            ua_str = log["Useragent"][1:-1]
            ua_parsed = uaparse(ua_str)
            if not ua_parsed.is_bot:
                browsers[ua_parsed.browser.family].add(ip)
                oses[ua_parsed.os.family].add(ip)
            ref = log["Referer"][1:-1].lower()
            ref = ref.replace('://www.', '://')
            p = urlparse(ref)
            if p.path.endswith('/'):
                p = p._replace(path=p.path[:-1])
            ref = f"{p.netloc}{p.path}"
            if ref != "-" and not any(s in ref for s in SKIP_REFS):
                refs[ref].add(ip)
    if html:
        generate_html(days, browsers, oses, refs, html)
    else:
        console_print(days, browsers, oses, refs)


if __name__ == "__main__":
    Fire(parse)
