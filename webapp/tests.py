from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase
from db.import_json import import_json


class PageTests(TestCase):
    def test_all_collection_pages_render(self):
        for path in ("/", "/projects/", "/teams/", "/participants/", "/roles/"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "YourRole")

    def test_detail_pages_render_and_missing_ids_return_404(self):
        for path in ("/projects/1/", "/teams/1/", "/participants/1/", "/roles/1/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)
        for path in ("/projects/999/", "/teams/999/", "/participants/999/", "/roles/999/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)

    def test_navigation_uses_named_urls_and_static_assets(self):
        response = self.client.get("/")
        self.assertContains(response, 'href="/teams/"')
        self.assertContains(response, "/static/webapp/css/site.css")

    def test_invalid_json_is_reported_without_a_server_error(self):
        with TemporaryDirectory() as directory:
            Path(directory, "projects.json").write_text("{invalid", encoding="utf-8")
            with patch("webapp.views.repository.data_dir", Path(directory)):
                response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Не удалось загрузить данные", status_code=503)


class SQLitePagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import_json()

    def test_sqlite_pages_render(self):
        for url in (
            "/database/",
            "/database/available-teams/?project=1",
            "/database/statistics/",
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_available_team_search_uses_selected_project(self):
        response = self.client.get(
            "/database/available-teams/", {"project": 1}
        )
        self.assertContains(response, "Команда Альфа")
        self.assertContains(response, "2")

    def test_statistics_show_role_names(self):
        response = self.client.get("/database/statistics/")
        self.assertContains(response, "Backend-разработчик")
        self.assertContains(response, "Тестировщик")
