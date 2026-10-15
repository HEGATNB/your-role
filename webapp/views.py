from functools import wraps

from django.shortcuts import render
from django.http import Http404

from models import Participant, Project, Role, Team
from storage import JSONRepository, StorageError
from db.database import get_connection

repository = JSONRepository()


def handle_storage_errors(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except StorageError:
            return render(
                request,
                "webapp/storage_error.html",
                status=503,
            )

    return wrapped


@handle_storage_errors
def home(request):
    projects = repository.list_projects()
    teams = repository.list_teams()
    participants = repository.list_participants()
    roles = repository.list_roles()
    return render(request, "webapp/home.html", {
        "projects": projects,
        "teams": teams,
        "participant_count": len(participants),
        "role_count": len(roles),
        "active_projects": sum(project.is_active for project in projects),
    })


def _list(request, template, key, context_key):
    rows = getattr(repository, f"list_{key}")()
    return render(request, template, {context_key: rows})


@handle_storage_errors
def projects(request):
    return render(request, "webapp/projects.html", {
        "projects": repository.list_projects(),
        "teams": repository.list_teams(),
    })


@handle_storage_errors
def teams(request):
    teams_list = repository.list_teams()
    projects_by_id = {project.id: project for project in repository.list_projects()}
    return render(request, "webapp/teams.html", {
        "teams": teams_list,
        "projects_by_id": projects_by_id,
    })


@handle_storage_errors
def participants(request):
    roles_by_id = {role.id: role for role in repository.list_roles()}
    return render(request, "webapp/participants.html", {
        "participants": repository.list_participants(), "roles_by_id": roles_by_id,
    })


@handle_storage_errors
def roles(request):
    return _list(request, "webapp/roles.html", "roles", "roles")


def _detail(request, model, object_id, template, context_key):
    obj = repository.get(model, object_id)
    if obj is None:
        raise Http404("Запись не найдена")
    return render(request, template, {context_key: obj})


@handle_storage_errors
def project_detail(request, object_id):
    return _detail(
        request, Project, object_id, "webapp/project_detail.html", "project"
    )


@handle_storage_errors
def team_detail(request, object_id):
    team = repository.get(Team, object_id)
    if team is None:
        raise Http404("Команда не найдена")
    participants_by_id = {
        item.id: item for item in repository.list_participants()
    }
    project = repository.get(Project, team.project_id)
    return render(request, "webapp/team_detail.html", {
        "team": team,
        "project": project,
        "participants": [
            participants_by_id[item_id]
            for item_id in team.participant_ids
            if item_id in participants_by_id
        ],
        "roles_by_id": {role.id: role for role in repository.list_roles()},
    })


@handle_storage_errors
def participant_detail(request, object_id):
    participant = repository.get(Participant, object_id)
    if participant is None:
        raise Http404("Участник не найден")
    role = (
        repository.get(Role, participant.assigned_role_id)
        if participant.assigned_role_id
        else None
    )
    return render(request, "webapp/participant_detail.html", {
        "participant": participant,
        "role": role,
    })


@handle_storage_errors
def role_detail(request, object_id):
    role = repository.get(Role, object_id)
    if role is None:
        raise Http404("Роль не найдена")
    assigned = [
        participant for participant in repository.list_participants()
        if participant.assigned_role_id == role.id
    ]
    return render(request, "webapp/role_detail.html", {"role": role, "participants": assigned})


def database_overview(request):
    """Show the project data read directly from the standalone SQLite layer."""
    with get_connection() as connection:
        projects = connection.execute(
            "SELECT id, name, deadline FROM projects ORDER BY deadline"
        ).fetchall()
        teams = connection.execute(
            """SELECT t.id, t.name, p.name AS project_name, t.max_size,
                      COUNT(tp.participant_id) AS member_count
               FROM teams t JOIN projects p ON p.id = t.project_id
               LEFT JOIN team_participants tp ON tp.team_id = t.id
               GROUP BY t.id, t.name, p.name, t.max_size ORDER BY t.name"""
        ).fetchall()
        participant_count = connection.execute(
            "SELECT COUNT(*) FROM participants"
        ).fetchone()[0]
    return render(request, "webapp/database_overview.html", {
        "projects": projects,
        "teams": teams,
        "participant_count": participant_count,
    })


def database_available_teams(request):
    """Filter teams with free seats for a project selected in the query string."""
    with get_connection() as connection:
        projects = connection.execute(
            "SELECT id, name FROM projects WHERE is_active = 1 ORDER BY name"
        ).fetchall()
        selected_id = request.GET.get("project")
        selected_id = int(selected_id) if selected_id and selected_id.isdigit() else None
        teams = []
        if selected_id is not None:
            teams = connection.execute(
                """SELECT t.id, t.name, t.max_size,
                          COUNT(tp.participant_id) AS member_count,
                          t.max_size - COUNT(tp.participant_id) AS free_slots
                   FROM teams t LEFT JOIN team_participants tp ON tp.team_id = t.id
                   WHERE t.project_id = ? GROUP BY t.id, t.name, t.max_size
                   HAVING t.max_size - COUNT(tp.participant_id) > 0
                   ORDER BY t.name""",
                (selected_id,),
            ).fetchall()
    return render(request, "webapp/database_available.html", {
        "projects": projects,
        "teams": teams,
        "selected_id": selected_id,
    })


def database_statistics(request):
    """Show role assignment totals and experience aggregates from SQLite."""
    with get_connection() as connection:
        rows = connection.execute(
            """SELECT r.id, r.name, COUNT(p.id) AS assigned_count,
                      AVG(p.experience) AS average_experience
               FROM roles r LEFT JOIN participants p ON p.assigned_role_id = r.id
               GROUP BY r.id, r.name ORDER BY assigned_count DESC, r.name"""
        ).fetchall()
        totals = connection.execute(
            """SELECT COUNT(*) AS participant_count,
                      AVG(experience) AS average_experience
               FROM participants"""
        ).fetchone()
    return render(request, "webapp/database_statistics.html", {
        "role_stats": rows,
        "participant_count": totals["participant_count"],
        "average_experience": totals["average_experience"],
    })
