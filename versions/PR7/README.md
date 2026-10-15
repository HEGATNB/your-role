# YourRole - версия ПР7

## Описание

ПР7 добавляет к проекту отдельную SQLite-базу. JSON-файлы остаются исходными данными; скрипт переноса загружает их в связанные таблицы, а SQL-представления Django читают результаты через стандартный модуль `sqlite3`.

## Состав базы

Таблицы `projects`, `teams`, `participants`, `roles`, `team_participants` и `participant_preferences` описаны в [`sql/schema.sql`](../../sql/schema.sql). Внешние ключи поддерживают связи между проектами, командами, участниками и ролями; для таблиц связей заданы составные первичные ключи.

## Реализация

- [`db/database.py`](../../db/database.py) открывает соединение, возвращает строки как `sqlite3.Row` и включает проверку внешних ключей.
- [`db/import_json.py`](../../db/import_json.py) инициализирует схему и импортирует JSON-данные.
- [`sql/queries.sql`](../../sql/queries.sql) содержит запросы предметной области с фильтрацией, JOIN, агрегатами и группировкой.
- [`webapp/views.py`](../../webapp/views.py) и SQL-шаблоны предоставляют обзор базы, поиск команд со свободными местами и статистику назначений.
- База находится в [`data/yourrole.sqlite3`](../../data/yourrole.sqlite3).

## Команды

```powershell
python -m db.import_json
python manage.py check
python manage.py runserver
```

Страницы SQLite: `/database/`, `/database/available-teams/` и `/database/statistics/`.

Эта папка содержит описание этапа; исходники находятся в корне репозитория.
