import typing as typ

import attr

MAYOR_URLS = [f"https://www.policylocal.nz/candidates/TA_{i:03}" for i in range(1, 77)]
DHB_URLS = [f"https://www.policylocal.nz/candidates/DHB_{i:02}" for i in range(1, 21)]
COUNCILLORS_URL_FORMATS = [
    f"https://www.policylocal.nz/candidates/WARD_{i:03}" + "{:02}" for i in range(1, 77)
]
REGIONAL_COUNCILLORS_URL_FORMATS = [
    f"https://www.policylocal.nz/candidates/CON_{i:02}" + "{:02}" for i in range(1, 16)
]


@attr.s
class Candidate:

    election: str = attr.ib()
    electorate: typ.Optional[str] = attr.ib()

    url: str = attr.ib()
    image: typ.Optional[str] = attr.ib()
    name: str = attr.ib()
    affiliation: typ.Optional[str] = attr.ib()
    why_stand: typ.Optional[str] = attr.ib()
    priorities: typ.List[str] = attr.ib()
    why_elect: typ.Optional[str] = attr.ib()
    before_politics: typ.Optional[str] = attr.ib()
    age: typ.Optional[str] = attr.ib()
    lives_in: typ.Optional[str] = attr.ib()

    social_media: typ.Dict[str, str] = attr.ib()

    def as_dict(self):
        return attr.asdict(self)


@attr.s
class Election:

    id: str = attr.ib()
    type: str = attr.ib()
    region: str = attr.ib()
    electorate: typ.Optional[str] = attr.ib()
    candidates: typ.List[Candidate] = attr.ib()

    def as_dict(self):
        return attr.asdict(self, recurse=True)
