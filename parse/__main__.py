import itertools
import json
import pathlib

from . import (
    COUNCILLORS_URL_FORMATS,
    DHB_URLS,
    MAYOR_URLS,
    REGIONAL_COUNCILLORS_URL_FORMATS,
)
from .load import InvalidPage, parse
from .visit import Requester

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "public/data"
LOOKUP = ROOT / "src/assets/data_lookup.json"
COMBINED = DATA / "combined.json"


def candidates_json_safe(candidates):
    return [c.as_dict() for c in candidates]


class Data:
    def __init__(self):
        self.r = Requester()
        self.data = {}
        self.grouped = {}
        self.named = {}

    def write(self):
        LOOKUP.write_text(
            json.dumps(
                {"grouped": self.grouped, "named": self.named}, sort_keys=True, indent=2
            )
        )
        COMBINED.write_text(json.dumps(self.data, sort_keys=True, indent=2))

    def persist(self, url):
        print(f"Requesting {url}")
        base_url, response = self.r.request(url)
        print(f"  Parsing {len(response)} bytes of response")
        election = parse(base_url, response)
        fname = f"{election.id}.json"
        self.data[election.id] = election.as_dict()
        self.grouped.setdefault(election.type, {}).setdefault(election.region, {})[
            election.electorate
        ] = election.id
        self.named[election.id] = fname
        (DATA / fname).write_text(
            json.dumps(election.as_dict(), sort_keys=True, indent=2)
        )
        print(f"  Written data to {fname}\n")
        return election, fname


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    d = Data()
    for url_group in [DHB_URLS, MAYOR_URLS]:
        for url in url_group:
            try:
                d.persist(url)
            except InvalidPage:
                print("Page didn't represent an election")
                pass
        d.write()
    for url_format_group in [
        COUNCILLORS_URL_FORMATS,
        REGIONAL_COUNCILLORS_URL_FORMATS,
    ]:
        for format in url_format_group:
            old_election_region = None
            for i in itertools.count(1):
                url = format.format(i)
                try:
                    election, _ = d.persist(url)
                except InvalidPage:
                    print("Page didn't represent an election")
                    break
                if old_election_region is not None:
                    assert (
                        old_election_region == election.region
                    ), f"{old_election_region} != {election.region}"
                old_election_region = election.region
            d.write()
    akl_local_board_format = "https://www.policylocal.nz/candidates/CB_076{:02}"
    for i in itertools.count(3):
        url = akl_local_board_format.format(i)
        try:
            d.persist(url)
        except InvalidPage:
            print("Page didn't represent an election")
            break
    d.write()


if __name__ == "__main__":
    main()
