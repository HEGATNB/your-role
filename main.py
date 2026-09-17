from datetime import date

participant_name = "Иван Петров"
participant_skill = "Python"
participant_experience = 2          # лет опыта

role_name = "Backend-разработчик"
role_required_skill = "Python"
role_min_experience = 1             # минимальный опыт, лет

project_name = "Учебный проект: Telegram-бот"
project_deadline = date(2026, 12, 15)
project_is_active = True

team_size = 4
max_team_size = 5

def is_participant_suitable(
    skill: str,
    experience: int,
    required_skill: str,
    min_experience: int,
) -> bool:
    if skill == required_skill and experience >= min_experience:
        return True
    return False

def can_add_to_team(current_size: int, limit: int, is_active: bool) -> bool:
    if not is_active:
        return False
    if current_size >= limit:
        return False
    return True

def get_assignment_status(
    suitable: bool,
    can_add: bool,
    participant: str,
    role: str,
) -> str:
    if not can_add:
        return f"Нельзя добавить {participant}: команда уже заполнена."
    if suitable:
        return f"{participant} может быть назначен на роль «{role}»."
    return f"{participant} не подходит на роль «{role}»."


def free_slots(current_size: int, limit: int) -> int:
    if current_size >= limit:
        return 0
    return limit - current_size


# Основной сценарий
def main() -> None:
    suitable = is_participant_suitable(
        participant_skill,
        participant_experience,
        role_required_skill,
        role_min_experience,
    )
    can_add = can_add_to_team(team_size, max_team_size, project_is_active)
    status = get_assignment_status(
        suitable, can_add, participant_name, role_name
    )
    slots = free_slots(team_size, max_team_size)

    print("=" * 50)
    print(f"Проект: {project_name}")
    print(f"Дедлайн: {project_deadline}")
    print(f"Активен: {'да' if project_is_active else 'нет'}")
    print("-" * 50)
    print(f"Участник: {participant_name}")
    print(f"Навык: {participant_skill}")
    print(f"Опыт: {participant_experience} лет")
    print("-" * 50)
    print(f"Роль: {role_name}")
    print(f"Требуемый навык: {role_required_skill}")
    print(f"Минимальный опыт: {role_min_experience} лет")
    print("-" * 50)
    print(f"Свободных мест в команде: {slots}")
    print(status)
    print("=" * 50)


if __name__ == "__main__":
    main()