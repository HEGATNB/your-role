from django.urls import path

from . import views

app_name = "webapp"
urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("projects/<int:object_id>/", views.project_detail, name="project_detail"),
    path("teams/", views.teams, name="teams"),
    path("teams/<int:object_id>/", views.team_detail, name="team_detail"),
    path("participants/", views.participants, name="participants"),
    path("participants/<int:object_id>/", views.participant_detail, name="participant_detail"),
    path("roles/", views.roles, name="roles"),
    path("roles/<int:object_id>/", views.role_detail, name="role_detail"),
]
