import gzip
from clfparser import CLFParser
from fire import Fire
from tqdm import tqdm


def parse(gz_path):
    refs = {}
    skips = ["subreply.com", "dubfi.com", "sublevel.net", "artificialfeed.com"]

    with gzip.open(gz_path, "rt") as f:
        for line in tqdm(f):
            log = CLFParser.logDict(line)
            ref = log["Referer"][1:-1]
            if ref != "-" and not any(s in ref for s in skips):
                if ref in refs:
                    refs[ref] += 1
                else:
                    refs[ref] = 1

    refs = {k: v for k, v in sorted(refs.items(), key=lambda item: item[1])}

    for k, v in refs.items():
        print(k, v)


if __name__ == "__main__":
    Fire(parse)
