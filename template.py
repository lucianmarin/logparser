TEMPLATE = """<!doctype html>
<html>
<head>
    <title>Logparser</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html { --black: black; --whitesmoke: #f0f0f0; --black: black; }
        @media (prefers-color-scheme: dark) {
            html { --white: black; --whitesmoke: #202020; --black: white; }
        }
        * { margin: 0; padding: 0; }
        body {
            background-color: var(--white);
            color: var(--black);
            font-family: Tahoma, Ubuntu, Cantarell, Oxygen, sans-serif;
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
        .section .even {
            background-color: var(--whitesmoke); border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="section">
        <h3>Days<sup>{{ days | length }}</sup></h3>
        {% for day, ips in days | reverse %}
            {% if ips | length > min_value %}
                <p class="{{ loop.cycle('odd', 'even') }}">
                    <span>{{ ips | length }}</span> {{ day }}
                </p>
            {% endif %}
        {% endfor %}
    </div>
    <div class="section">
        <h3>Browsers<sup>{{ browsers | length }}</sup></h3>
        {% for browser, ips in browsers | reverse %}
            {% if ips | length > min_value %}
                <p class="{{ loop.cycle('odd', 'even') }}">
                    <span>{{ ips | length }}</span> {{ browser }}
                </p>
            {% endif %}
        {% endfor %}
    </div>
    <div class="section">
        <h3>Operating Systems<sup>{{ systems | length }}</sup></h3>
        {% for system, ips in systems | reverse %}
            {% if ips | length > min_value %}
                <p class="{{ loop.cycle('odd', 'even') }}">
                    <span>{{ ips | length }}</span> {{ system }}
                </p>
            {% endif %}
        {% endfor %}
    </div>
    <div class="section">
        <h3>Referrers<sup>{{ refs | length }}</sup></h3>
        {% for ref, ips in refs | reverse %}
            {% if ips | length > min_value %}
                <p class="{{ loop.cycle('odd', 'even') }}">
                    <span>{{ ips | length }}</span> {{ ref }}
                </p>
            {% endif %}
        {% endfor %}
    </div>
</body>
</html>
"""
