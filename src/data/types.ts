

interface ICandidate {
  election: string
  electorate?: string
  url: string
  image?: string
  name: string
  affiliation?: string
  whyStand?: string
  priorities: string[]
  whyElect?: string
  beforePolitics?: string
  age?: string
  livesIn?: string
  socialMedia: Map<string, string>
}
interface IElection {
  id: string
  type: string
  region: string
  electorate?: string
  candidates: Candidate[]
}

export class Candidate implements ICandidate {
  election: string

  electorate?: string

  url: string

  image?: string

  name: string

  affiliation?: string

  livesIn?: string

  priorities: string[]

  whyElect?: string

  beforePolitics?: string

  age?: string

  socialMedia: Map<string, string>

  whyStand?: string

  constructor(obj: ICandidate) {
    this.election = obj.election;
    this.electorate = obj.electorate;
    this.url = obj.url;
    this.image = obj.image;
    this.name = obj.name;
    this.affiliation = obj.affiliation;
    this.whyStand = obj.whyStand;
    this.priorities = obj.priorities;
    this.whyElect = obj.whyElect;
    this.beforePolitics = obj.beforePolitics;
    this.age = obj.age;
    this.livesIn = obj.livesIn;
    this.socialMedia = obj.socialMedia;
  }

  static initialize(obj: any): Candidate {
    return new Candidate({
      election: obj.election,
      electorate: obj.electorate,
      url: obj.url,
      image: obj.image,
      name: obj.name,
      affiliation: obj.affiliation,
      whyStand: obj.why_stand,
      priorities: obj.priorities,
      whyElect: obj.why_elect,
      beforePolitics: obj.before_politics,
      age: obj.age,
      livesIn: obj.lives_in,
      socialMedia: new Map(Object.entries(obj.social_media)),
    });
  }
}

export class Election implements IElection {
  id: string

  type: string

  region: string

  electorate?: string | undefined

  candidates: Candidate[]

  constructor(obj: IElection) {
    this.id = obj.id;
    this.type = obj.type;
    this.region = obj.region;
    this.electorate = obj.electorate;
    this.candidates = obj.candidates;
  }

  static initialize(obj: any) : Election {
    return new Election({
      id: obj.id,
      type: obj.type,
      region: obj.region,
      electorate: obj.electorate,
      candidates: (obj.candidates as [any]).map(candidate => Candidate.initialize(candidate)),
    });
  }
}
