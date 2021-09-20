TEMPLATE = """<!doctype html>
<html>
<head>
    <title>Logparser</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, user-scalable=0">
    <style>
        * { margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            font-size: 13px;
            line-height: 20px;
        }
        .section {
            margin: 0 auto;
            max-width: 480px;
            padding-top: 10px;
        }
        .section h3 { margin-left: 10px; }
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
        .section .even { background-color: whitesmoke; }
    </style>
</head>
<body>
    <div class="section">
        <h3>Days</h3>
        {% for day, ips in days | reverse -%}
            <p class="{{ loop.cycle('odd', 'even') }}"><span>{{ ips | length }}</span> {{ day }}</p>
        {%- endfor %}
    </div>
    <div class="section">
        <h3>Browsers</h3>
        {% for browser, ips in browsers | reverse -%}
            <p class="{{ loop.cycle('odd', 'even') }}"><span>{{ ips | length }}</span> {{ browser }}</p>
        {%- endfor %}
    </div>
    <div class="section">
        <h3>Operating Systems</h3>
        {% for os, ips in oses | reverse -%}
            <p class="{{ loop.cycle('odd', 'even') }}"><span>{{ ips | length }}</span> {{ os }}</p>
        {%- endfor %}
    </div>
    <div class="section">
        <h3>Referrers</h3>
        {% for ref, ips in refs | reverse -%}
            <p class="{{ loop.cycle('odd', 'even') }}"><span>{{ ips | length }}</span> {{ ref }}</p>
        {%- endfor %}
    </div>
</body>
</html>"""
