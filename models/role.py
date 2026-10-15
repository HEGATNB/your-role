from dataclasses import dataclass


@dataclass
class Role:
    id: int
    name: str
    description: str
    required_skill: str
    min_experience: int = 0

    def __str__(self) -> str:
        return self.name
