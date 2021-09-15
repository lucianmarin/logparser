# Logparser

Command line parser for common log format (Nginx default).

## Usage

It counts most important data: refferers, operating systems and browsers.

```shell
python parse.py site_name.log.gz
```

## Output

Output for [Subreply](https://subreply.com/) for a day in Sep, 2021:

```shell
--- OS
4 KaiOS
13 Other
97 Ubuntu
129 Linux
274 iOS
533 Android
731 Mac OS X
43743 Windows

--- Browser
2 Bytespider
4 Mobile Safari UI/WKWebView
6 IE
6 Chrome Mobile iOS
6 Opera
13 Go-http-client
16 Opera Mobile
22 Firefox iOS
150 Safari
158 Firefox Mobile
177 Chrome Mobile WebView
184 Chrome Mobile
203 Edge
242 Mobile Safari
689 Firefox
43646 Chrome

--- Referer
1 news.ycombinator.com
2 twtxt.net/conv/j3qpzuq
2 192.168.1.23:9000
2 t.co/n2isdf2m3f
2 old.reddit.com/r/redditalternatives/comments/oioeot/list_of_active_reddit_alternatives_v7
2 m.youtube.com
2 lobste.rs/threads
2 it.reddit.com/r/internetisbeautiful
2 1mb.club
2 reddit.com/r/internetisbeautiful
4 twtxt.net
4 ro.linkedin.com
4 199.247.2.88
6 out.reddit.com/t3_pl9hiu
6 sjmulder.nl/en/textonly.html
7 lucianmarin.com
7 binance.com
8 google.com
10 sjmulder.nl
23 lobste.rs
30 reddit.com
181 lobste.rs/s/8fzzmz/what_are_you_doing_this_week
```
