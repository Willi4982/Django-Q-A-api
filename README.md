# Q&A API Service (Django + DRF + PostgreSQL)

## Стек
- Django 5 + Django REST Framework
- PostgreSQL
- Docker + docker-compose
- Миграции через Django ORM
- Тесты: pytest + pytest-django

## Эндпоинты
- GET `/questions/` — список всех вопросов
- POST `/questions/` — создать новый вопрос
- GET `/questions/{id}` — получить вопрос и все ответы
- DELETE `/questions/{id}` — удалить вопрос (и его ответы каскадно)
- POST `/questions/{id}/answers/` — добавить ответ к вопросу
- GET `/answers/{id}` — получить конкретный ответ
- DELETE `/answers/{id}` — удалить ответ

### Простой UI (шаблоны Django)
- UI список вопросов: `http://127.0.0.1:8000/ui/questions/`
- UI детальная вопроса: `http://127.0.0.1:8000/ui/questions/<id>/`

## Запуск в Docker

```bash
docker-compose up --build
```

Сервис поднимется на `http://localhost:8000/`.

## Локальная разработка (Windows, через venv)

1) Активируйте venv:

```powershell
& "C:\Users\Willi\Desktop\test\.venv\Scripts\Activate.ps1"
```

2) Установите зависимости:

```powershell
pip install -r requirements.txt
```

3) Настройте переменные окружения (если хотите использовать локальный PostgreSQL), либо запустите через Docker.

4) Примените миграции и запустите сервер:

```powershell
python manage.py migrate
python manage.py runserver
```

## Миграции
Миграции генерируются командой:

```bash
python manage.py makemigrations qa
python manage.py migrate
```

## Тесты

```bash
pytest -q
```

## Валидация и бизнес-логика
- Ответ нельзя создать для несуществующего вопроса (проверка при создании).
- Один пользователь может оставлять несколько ответов на один вопрос.
- При удалении вопроса ответы удаляются каскадно (`on_delete=models.CASCADE`).


