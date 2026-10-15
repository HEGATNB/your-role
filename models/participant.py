from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role


@dataclass
class Participant:
    id: int
    name: str
    email: str
    skills: list[str] = field(default_factory=list)
    experience: int = 0
    preferred_role_ids: list[int] = field(default_factory=list)
    assigned_role_id: int | None = None

    def is_suitable_for(self, role: "Role") -> bool:
        return role.required_skill in self.skills and self.experience >= role.min_experience

    def assign_role(self, role: "Role") -> bool:
        if not self.is_suitable_for(role):
            return False
        self.assigned_role_id = role.id
        return True

    def __str__(self) -> str:
        return f"{self.name} ({', '.join(self.skills) or 'навыки не указаны'})"
