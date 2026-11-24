#!/usr/bin/env python3
"""
search-ddg.py
=============
DuckDuckGo Lite search via Python subprocess.

Python's ssl module generates a different TLS fingerprint than Node.js OpenSSL,
which bypasses DuckDuckGo's bot-detection (JA3 fingerprinting). This script is
invoked by the web_search MCP tool as a child process.

Reads  JSON from stdin:  {"query": "...", "proxy": "http://..."}
Writes JSON to stdout:   {"results": [{title, url, snippet}...]}
                      or {"error": "..."}
"""

import html as _html
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception as exc:
        print(json.dumps({"error": f"Invalid input JSON: {exc}"}))
        sys.exit(0)

    query = data.get("query", "")
    proxy = data.get("proxy", "")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    proxy_dict = {"https": proxy, "http": proxy} if proxy else {}
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(proxy_dict),
        urllib.request.HTTPSHandler(context=ctx),
    )

    post_data = urllib.parse.urlencode({"q": query, "b": "", "kl": "us-en"}).encode()
    req = urllib.request.Request(
        "https://lite.duckduckgo.com/lite/",
        data=post_data,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        with opener.open(req, timeout=15) as resp:
            page = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        print(json.dumps({"error": f"HTTP {exc.code}: {exc.reason}"}))
        sys.exit(0)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        sys.exit(0)

    def strip_tags(s):
        return re.sub(r"<[^>]+>", "", s).strip()

    def clean(s):
        return " ".join(_html.unescape(strip_tags(s)).split())

    link_pat = re.compile(
        r'<a[^>]+href=[\'"]([^\'"]+)[\'"][^>]+class=[\'"]result-link[\'"][^>]*>(.*?)</a>',
        re.S,
    )
    snip_pat = re.compile(r"class=['\"]result-snippet['\"][^>]*>(.*?)</td>", re.S)

    links = [(clean(m.group(2)), m.group(1)) for m in link_pat.finditer(page)]
    snippets = [clean(m.group(1)) for m in snip_pat.finditer(page)]

    results = [
        {
            "title": title,
            "url": url,
            "snippet": snippets[i] if i < len(snippets) else "",
        }
        for i, (title, url) in enumerate(links)
    ]

    print(json.dumps({"results": results}))


if __name__ == "__main__":
    main()
