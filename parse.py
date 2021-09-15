import gzip
from urllib.parse import urlparse

import user_agents as ua
from clfparser import CLFParser
from fire import Fire
from tqdm import tqdm


def reverse(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}


def parse(gz_path):
    refs = {}
    browsers = {}
    oses = {}
    skips = [
        "subreply.com", "dubfi.com", "sublevel.net",
        "artificialfeed.com", "unfeeder.com", "radfi.com"
    ]

    with gzip.open(gz_path, "rt") as f:
        for line in tqdm(f):
            log = CLFParser.logDict(line)
            ua_str = log["Useragent"][1:-1]
            ua_parsed = ua.parse(ua_str)
            if not ua_parsed.is_bot:
                if ua_parsed.browser.family in browsers:
                    browsers[ua_parsed.browser.family] += 1
                else:
                    browsers[ua_parsed.browser.family] = 1
                if ua_parsed.os.family in oses:
                    oses[ua_parsed.os.family] += 1
                else:
                    oses[ua_parsed.os.family] = 1
            ref = log["Referer"][1:-1].lower()
            ref = ref.replace("://www.", "://")
            p = urlparse(ref)
            if p.path.endswith('/'):
                p = p._replace(path=p.path[:-1])
            ref = f"{p.netloc}{p.path}"
            if ref != "-" and not any(s in ref for s in skips):
                if ref in refs:
                    refs[ref] += 1
                else:
                    refs[ref] = 1

    refs = reverse(refs)
    browsers = reverse(browsers)
    oses = reverse(oses)

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
