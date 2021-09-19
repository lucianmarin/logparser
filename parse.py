import gzip
from collections import defaultdict
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from tqdm import tqdm
from user_agents import parse as uaparse

SKIP_REFS = ["subreply.com", "unfeeder.com"]


def parse(gz_path):
    ips = defaultdict(set)
    browsers = defaultdict(set)
    oses = defaultdict(set)
    refs = defaultdict(set)

    with gzip.open(gz_path, "rt") as file:
        for line in tqdm(file):
            log = CLFParser.logDict(line)
            ip = log['h']
            day = log['time'].strftime('%Y-%m-%d %a')
            ips[day].add(ip)

            ua_str = log["Useragent"][1:-1]
            ua_parsed = uaparse(ua_str)
            if not ua_parsed.is_bot:
                browsers[ua_parsed.browser.family].add(ip)
                oses[ua_parsed.os.family].add(ip)

            ref = log["Referer"][1:-1].lower()
            ref = ref.replace("://www.", "://")
            p = urlparse(ref)
            if p.path.endswith('/'):
                p = p._replace(path=p.path[:-1])
            ref = f"{p.netloc}{p.path}"
            if ref != "-" and not any(s in ref for s in SKIP_REFS):
                refs[ref].add(ip)

    print('---- IP')
    for k, v in sorted(ips.items()):
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


if __name__ == "__main__":
    Fire(parse)
