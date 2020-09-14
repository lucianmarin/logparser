import gzip
import user_agents as ua
from fire import Fire
from tqdm import tqdm

from clfparser import CLFParser


def reverse(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}


def parse(gz_path):
    refs = {}
    browsers = {}
    oses = {}
    skips = ["subreply.com", "dubfi.com", "sublevel.net", "artificialfeed.com"]

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
            ref = log["Referer"][1:-1]
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
        print(k, v)

    print("--- Browser")
    for k, v in browsers.items():
        print(k, v)

    print("--- Referer")
    for k, v in refs.items():
        print(k, v)


if __name__ == "__main__":
    Fire(parse)
