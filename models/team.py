from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .participant import Participant


@dataclass
class Team:
    id: int
    name: str
    project_id: int
    max_size: int
    participant_ids: list[int] = field(default_factory=list)

    @property
    def free_slots(self) -> int:
        return max(0, self.max_size - len(self.participant_ids))

    def add_participant(self, participant_id: int | "Participant") -> bool:
        participant_id = getattr(participant_id, "id", participant_id)
        if participant_id in self.participant_ids or self.free_slots == 0:
            return False
        self.participant_ids.append(participant_id)
        return True

    def remove_participant(self, participant_id: int) -> bool:
        if participant_id not in self.participant_ids:
            return False
        self.participant_ids.remove(participant_id)
        return True

    def __str__(self) -> str:
        return self.name
