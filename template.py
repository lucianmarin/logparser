TEMPLATE = """<!doctype html>
<html>
<head>
    <title>Logparser</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; }
        body {
            font-family: Tahoma, Noto Sans, Roboto, Oxygen, Ubuntu,
                         Cantarell, sans-serif;
            font-size: 13px;
            line-height: 20px;
        }
        sup { line-height: 0; }
        h3 sup { font-size: 11px; margin-left: 1px; }
        .section {
            margin: 0 auto;
            max-width: 480px;
            padding: 0 10px;
            padding-top: 10px;
        }
        .section:last-child { padding-bottom: 20px; }
        .section p {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .section span {
            float: left;
            margin-right: 10px;
            text-align: right;
            width: 20%;
        }
        .section .even { background-color: whitesmoke; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="section">
        <h3>Days<sup>{{ days | length }}</sup></h3>
        {% for day, ips in days | reverse %}
            <p class="{{ loop.cycle('odd', 'even') }}">
                <span>{{ ips | length }}</span> {{ day }}
            </p>
        {% endfor %}
    </div>
    <div class="section">
        <h3>Browsers<sup>{{ browsers | length }}</sup></h3>
        {% for browser, ips in browsers | reverse %}
            <p class="{{ loop.cycle('odd', 'even') }}">
                <span>{{ ips | length }}</span> {{ browser }}
            </p>
        {% endfor %}
    </div>
    <div class="section">
        <h3>Operating Systems<sup>{{ oses | length }}</sup></h3>
        {% for os, ips in oses | reverse %}
            <p class="{{ loop.cycle('odd', 'even') }}">
                <span>{{ ips | length }}</span> {{ os }}
            </p>
        {% endfor %}
    </div>
    <div class="section">
        <h3>Referrers<sup>{{ refs | length }}</sup></h3>
        {% for ref, ips in refs | reverse %}
            <p class="{{ loop.cycle('odd', 'even') }}">
                <span>{{ ips | length }}</span> {{ ref }}
            </p>
        {% endfor %}
    </div>
</body>
</html>
"""
