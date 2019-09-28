import functools
import json
import pathlib
import re

import attr
import bs4
import requests

ROOT = pathlib.Path(__file__).parent.parent
CACHE_DIR = ROOT / "localcache"


@attr.s
class Requester:

    session = attr.ib(factory=requests.Session, repr=False, cmp=False)

    def _request(self, url):
        with self.session.get(url) as response:
            response.raise_for_status()
            return response.url, response.text

    def request(self, url):
        a, _, b = url.partition("https://www.policylocal.nz/candidates/")
        if b:
            # Can use cache
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            file = CACHE_DIR / f"{b}.json"
            try:
                data = json.loads(file.read_text())
                return data["base_url"], data["content"]
            except Exception:
                print("  Error using cache")
                base_url, content = self._request(url)
                file.write_text(
                    json.dumps({"url": url, "base_url": base_url, "content": content})
                )
                return base_url, content
        else:
            return self._request(url)
