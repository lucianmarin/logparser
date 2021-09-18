import gzip
from collections import defaultdict
from urllib.parse import urlparse

from clfparser import CLFParser
from fire import Fire
from tqdm import tqdm
from user_agents import parse as uaparse

SKIP_REFS = ["subreply.com", "unfeeder.com"]


def order(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}


def parse(gz_path):
    refs = defaultdict(int)
    browsers = defaultdict(int)
    oses = defaultdict(int)

    with gzip.open(gz_path, "rt") as file:
        for line in tqdm(file):
            log = CLFParser.logDict(line)
            ua_str = log["Useragent"][1:-1]
            ua_parsed = uaparse(ua_str)
            if not ua_parsed.is_bot:
                browsers[ua_parsed.browser.family] += 1
                oses[ua_parsed.os.family] += 1
            ref = log["Referer"][1:-1].lower()
            ref = ref.replace("://www.", "://")
            p = urlparse(ref)
            if p.path.endswith('/'):
                p = p._replace(path=p.path[:-1])
            ref = f"{p.netloc}{p.path}"
            if ref != "-" and not any(s in ref for s in SKIP_REFS):
                refs[ref] += 1

    refs = order(refs)
    browsers = order(browsers)
    oses = order(oses)

    print("--- OS")
    for k, v in oses.items():
        print(v, k)

    print("\n--- Browser")
    for k, v in browsers.items():
        print(v, k)

    print("\n--- Referer")
    for k, v in refs.items():
        print(v, k)


if __name__ == "__main__":
    Fire(parse)
