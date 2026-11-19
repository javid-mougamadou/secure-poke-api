from dataclasses import dataclass


@dataclass
class CurrentUser:
    id: int
    username: str
    email: str
    groups: list[str]

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            groups=data['groups'],
        )
