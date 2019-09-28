import functools
import pathlib
import re
import typing as typ

import attr
import bs4
import requests

from . import Candidate, Election

FRAGMENT_RE = re.compile(
    r'[0-9`~!@#$%^&*()_|+\=?;:\'"’,.<>\{\}\[\]\\\/]', re.IGNORECASE
)


class InvalidPage(Exception):
    pass


@functools.lru_cache(maxsize=1)
def bs4_loader():
    for loader in ["lxml", "html.parser"]:
        try:
            bs4.BeautifulSoup("<html></html>", loader)
            return loader
        except:
            pass
    raise ValueError("Cannot find a suitable loader")


def none_if_default(value, default):
    return None if value == default else value


def text_if_present(soup):
    if soup:
        return "".join(soup.stripped_strings)
    else:
        return None


def parse(base_url, content):
    _, _, id = base_url.strip("/").rpartition("/")
    soup = bs4.BeautifulSoup(content, bs4_loader())
    print("  ", soup.title)
    if "field_electiontitle" in soup.title.string:
        raise InvalidPage()
    type, election, a_electorate = parse_election(
        "".join(soup.find("h1").stripped_strings)
    )
    b_electorate = parse_electorate(
        "".join(soup.find(class_="views-field-field-subtitle").stripped_strings)
    )
    if a_electorate is None:
        electorate = b_electorate
    else:
        assert b_electorate is not None, f"{a_electorate!r}  {b_electorate!r}"
        assert a_electorate == b_electorate, f"{a_electorate!r}  {b_electorate!r}"
        electorate = a_electorate
    print(f"  {election!r} | {electorate!r}")
    return Election(
        id,
        type,
        election,
        electorate,
        [
            parse_candidate(base_url, election, electorate, candidate)
            for candidate in soup.find_all(class_="candidate")
        ],
    )


def parse_election(heading):
    type, name, ward = None, heading, None
    if heading.endswith(" Ward)"):
        useful, _, _ = heading.partition(" Ward)")
        name, _, ward = useful.partition(" (")
    elif "(" in heading or ")" in heading:
        raise ValueError("Possible invalid election")

    if name.endswith(" Regional Council"):
        name, _, _ = name.partition(" Regional Council")
        type = "Regional Council"
    elif name.endswith(" District Council"):
        name, _, _ = name.partition(" District Council")
        type = "Council"
    elif name.endswith(" City Council"):
        name, _, _ = name.partition(" City Council")
        type = "Council"
    elif name.endswith(" Council"):
        name, _, _ = name.partition(" Council")
        type = "Council"
    elif name.endswith(" Local Board"):
        name, _, _ = name.partition(" Local Board")
        type = "Local Board"
    elif name.endswith(" DHB"):
        name, _, _ = name.partition(" DHB")
        type = "DHB"
    elif name.startswith("Mayor of ") and name.endswith(" District"):
        name, _, _ = name.partition(" District")
        _, _, name = name.partition("Mayor of")
        type = "Mayor"
    elif name.startswith("Mayor of "):
        _, _, name = name.partition("Mayor of")
        type = "Mayor"
    else:
        raise ValueError(f"Unknown election {name} / {heading}")
    if type == "Council" and name.startswith("Mayor of "):
        _, _, name = name.partition("Mayor of")
        type = "Mayor"

    return type, name, ward


def parse_electorate(subtitle):
    if subtitle.startswith("Your vote for the members of"):
        # DHB & local board(for Auckland)
        return None
    elif subtitle.startswith("Your vote for the mayor of"):
        return None
    elif subtitle.startswith("Uncontested: there will be no vote "):
        _, _, part = subtitle.partition("Uncontested: there will be no ")
        return parse_electorate(f"Your {part}")
    elif " Ward/" in subtitle:
        a, _, b = subtitle.rpartition(" Ward/")
        return parse_electorate(f"{a}/{b} Ward")
    elif subtitle.startswith("Your vote for the councillors for the"):
        _, _, area = subtitle.partition("Your vote for the councillors for the")
        return parse_electorate_area(area)
    elif subtitle.startswith("Your vote for the councillor for the"):
        _, _, area = subtitle.partition("Your vote for the councillor for the")
        return parse_electorate_area(area)
    else:
        raise ValueError(f"Unknown electorate type: {subtitle}")


def parse_electorate_area(area):
    if area.endswith("Ward"):
        electorate, _, _ = area.rpartition("Ward")
        assert electorate, f"{area} => Ward"
    elif area.endswith("Constituency"):
        electorate, _, _ = area.rpartition("Constituency")
        assert electorate, f"{area} => Constituency"
    else:
        raise ValueError(f"Unknown councillor type: {area}")
    return electorate.strip()


def parse_candidate(base_url, election, electorate, soup):
    fname = text_if_present(soup.find(class_="field-name-field-first-name")) or ""
    lname = text_if_present(soup.find(class_="field-name-field-last-name")) or ""
    name = f"{fname} {lname}"
    fragment = FRAGMENT_RE.sub("", f"{fname} {lname}")

    extras = {}

    return Candidate(
        election=election,
        electorate=electorate,
        url=f"{base_url}#{fragment}",
        name=name,
        image=none_if_default(
            soup.find(class_="field-name-field-image").find("img")["src"],
            "https://www.policylocal.nz/sites/default/files/styles/round_portrait/public/default_images/default_profile_image.png?itok=bTqalX0V",
        ),
        affiliation=text_if_present(soup.find(class_="field-name-field-affiliation")),
        why_stand=parse_headered_section(soup.find(class_="field-name-field-cq-5")),
        priorities=parse_priorities(soup.find(class_="field-name-field-cq-5")),
        why_elect=parse_headered_section(soup.find(class_="field-name-field-cq-9")),
        before_politics=parse_headered_section(
            soup.find(class_="field-name-field-cq-2")
        ),
        age=parse_headered_section(soup.find(class_="field-name-field-cq-3")),
        lives_in=parse_headered_section(soup.find(class_="field-name-field-cq-4")),
        social_media=parse_social_media(soup.find(class_="group-social")),
    )


def parse_headered_section(soup):
    content = "".join(c for c in soup.children if isinstance(c, bs4.NavigableString))
    return none_if_default(content, "No response given")


def parse_priorities(soup):
    # This will return an empty list if the content is `No response given`
    return ["".join(p.stripped_strings) for p in soup.find_all(class_="priority")]


def parse_social_media(soup):
    if not soup:
        return {}
    social = {}
    for e in soup.find_all(class_="item-list"):
        media_type = e["id"]
        _, _, media_type = media_type.partition("linkicon-node-candidate-field-")
        media_type, _, _ = media_type.rpartition("-")
        assert media_type, e["id"]
        social[media_type] = e.find("a")["href"]
