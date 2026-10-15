from dataclasses import dataclass
from datetime import date


@dataclass
class Project:
    id: int
    name: str
    description: str
    deadline: date
    is_active: bool = True

    def days_until_deadline(self, today: date | None = None) -> int:
        return (self.deadline - (today or date.today())).days

    def __str__(self) -> str:
        return self.name
