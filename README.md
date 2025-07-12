# Logparser

Command line parser for common log format (Nginx default).

## Usage

It counts most important data: referrers, operating systems, browsers and daily unique visitors (IPs). It excludes bots by default.

```shell
# Console output
python parse.py sitename.log.gz

# Hide less than or equal values
python parse.py sitename.log.gz --hide 1

# HTML output
python parse.py sitename.log.gz --html ~/sitename/logs.html

# Ignore hostnames from referrers
python parse.py sitename.log.gz --skip "subreply.com"
```

Install and update PIP packages.

```shell
pip install -U -r requirements.txt
```

## Speed

- Logparser 24,249/s
- GoAccess 1.3 6,234/s - virtual server, Intel (1 core)
- GoAccess 1.5 47,299/s - laptop, Intel (4 cores)

## Outputs

- HTML output is based on Jinja2 templates. It can be improved as you see fit.
- Console output for [Subreply](https://subreply.com/) for a fews days in Sep, 2021:

```shell
----- Days
 1402 2021-09-14 Tuesday
  893 2021-09-15 Wednesday
  797 2021-09-16 Thursday
  857 2021-09-17 Friday
  951 2021-09-18 Saturday
  945 2021-09-19 Sunday
  869 2021-09-20 Monday

----- Browsers
    2 Chrome Mobile iOS
    2 Bytespider
    2 HeadlessChrome
    3 Links
    4 Firefox iOS
    4 UC Browser
    6 IE
    7 Go-http-client
    7 Opera
    8 Other
   20 Chrome Mobile WebView
   20 Edge
   28 Firefox Mobile
   30 Safari
   42 Chrome Mobile
   56 Mobile Safari
  111 Firefox
 3468 Chrome

----- Operating Systems
   15 Other
   22 Ubuntu
   39 Linux
   63 iOS
   91 Android
  101 Mac OS X
 3474 Windows

----- Referrers
    2 twtxt.net
    2 l.instagram.com
    2 lobste.rs/s/bffayk/what_are_you_doing_this_weekend
    3 ro.linkedin.com
    3 199.247.2.88:80
    3 t.co/sv4adihlka
    3 lobste.rs/s/fe2eph/what_are_you_doing_this_weekend
    4 news.ycombinator.com
    4 1mb.club
    4 old.reddit.com/r/internetisbeautiful
    4 baidu.com
    4 t.co
    5 out.reddit.com/t3_pl9hiu
    5 sjmulder.nl/en/textonly.html
    8 nt
   10 199.247.2.88
   11 lobste.rs
   13 sjmulder.nl
   15 google.com
   16 lucianmarin.com
   49 reddit.com
   85 lobste.rs/s/8fzzmz/what_are_you_doing_this_week
```
