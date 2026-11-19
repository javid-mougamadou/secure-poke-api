from dataclasses import dataclass


@dataclass
class PokemonReference:
    name: str
    url: str

    @property
    def id(self):
        return int(self.url.rstrip('/').rsplit('/', 1)[-1])

    @classmethod
    def from_dict(cls, data):
        return cls(name=data['name'], url=data['url'])


@dataclass
class Pokemon:
    id: int
    name: str
    types: list[str]

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            types=[item['type']['name'] for item in data['types']],
        )
