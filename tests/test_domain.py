from datetime import date

from models import Participant, Project, Role, Team
from storage import JSONRepository, StorageError
from utils import recommend_role


def test_role_matching_and_assignment():
    participant = Participant(7, "Иван", "ivan@example.edu", ["Python"], 2)
    role = Role(3, "Backend", "Разработка", "Python", 1)
    assert participant.is_suitable_for(role)
    assert participant.assign_role(role)
    assert participant.assigned_role_id == role.id
    unsuitable = Role(4, "Дизайнер", "Интерфейс", "Figma", 0)
    assert not participant.assign_role(unsuitable)


def test_team_capacity_is_enforced():
    team = Team(1, "Альфа", 1, 1)
    assert team.add_participant(7)
    assert not team.add_participant(8)
    assert team.free_slots == 0
    assert team.remove_participant(7)
    assert team.free_slots == 1


def test_json_repository_loads_sample_entities():
    repository = JSONRepository()
    assert repository.list_projects()[0].deadline == date(2026, 12, 15)
    assert len(repository.list_participants()) == 3
    assert repository.get(Project, 1) is not None


def test_repository_saves_updated_entities(tmp_path):
    repository = JSONRepository(tmp_path)
    project = Project(1, "Командный проект", "Описание", date(2026, 12, 15))
    repository.save(project)
    assert repository.get(Project, 1) == project


def test_repository_reports_malformed_json(tmp_path):
    (tmp_path / "projects.json").write_text("{invalid", encoding="utf-8")
    repository = JSONRepository(tmp_path)
    try:
        repository.list_projects()
    except StorageError as error:
        assert "projects.json" in str(error)
    else:
        raise AssertionError("Malformed JSON should raise StorageError")


def test_team_interacts_with_participant_and_recommends_preference():
    participant = Participant(8, "Анна", "anna@example.edu", ["Python"], 2, [2])
    team = Team(2, "Бета", 1, 2)
    assert team.add_participant(participant)
    assert team.participant_ids == [participant.id]
    roles = [
        Role(1, "Backend", "Разработка", "Python", 1),
        Role(2, "Python mentor", "Наставник", "Python", 2),
    ]
    assert recommend_role(participant, roles) == roles[1]
