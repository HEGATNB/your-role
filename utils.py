from models import Participant, Role


def get_assignment_status(participant: Participant, role: Role) -> str:
    if participant.is_suitable_for(role):
        return f"{participant.name} подходит на роль «{role.name}»."
    return f"{participant.name} пока не подходит на роль «{role.name}»."


def recommend_role(participant: Participant, roles: list[Role]) -> Role | None:
    suitable = [role for role in roles if participant.is_suitable_for(role)]
    preferred = next(
        (role for role in suitable if role.id in participant.preferred_role_ids),
        None,
    )
    return preferred or (suitable[0] if suitable else None)
