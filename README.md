# FastAPI Test Backend

Простое тестовое приложение на FastAPI, возвращающее текущую дату и время.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
uvicorn main:app --reload
```

## API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Приветственное сообщение |
| GET | `/date` | Возвращает текущую дату (YYYY-MM-DD) |

## Примеры ответов

### GET /date
```json
{
  "date": "2025-01-15"
}
```

## Документация

После запуска приложения документация API доступна по адресу:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Стек технологий

- [FastAPI](https://fastapi.tiangolo.com/) — современный веб-фреймворк
- [Uvicorn](https://www.uvicorn.org/) — ASGI сервер
