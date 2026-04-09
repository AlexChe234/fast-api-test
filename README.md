# FastAPI Test Backend

Простое тестовое приложение на FastAPI, возвращающее текущую дату и время.

## Установка

### Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
uvicorn main:app --reload
```

### Docker

1. Соберите образ:
```bash
docker build -t fastapi-app .
```

2. Запустите контейнер:
```bash
docker run -p 8000:8000 fastapi-app
```

## API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Приветственное сообщение |
| GET | `/date` | Возвращает текущую дату (YYYY-MM-DD) |
| GET | `/date/{date_format}` | Возвращает текущую дату в указанном формате |

## Примеры ответов

### GET /date
```json
{
  "date": "2025-01-15"
}
```

### GET /date/{date_format}

Примеры запросов и ответов:

**Запрос:** `/date/%Y-%m-%d`
```json
{
  "date": "2025-01-15",
  "format": "%Y-%m-%d"
}
```

**Запрос:** `/date/%d.%m.%Y`
```json
{
  "date": "15.01.2025",
  "format": "%d.%m.%Y"
}
```

**Запрос:** `/date/%A, %d %B %Y`
```json
{
  "date": "Wednesday, 15 January 2025",
  "format": "%A, %d %B %Y"
}
```

**Популярные форматы:**
- `%Y-%m-%d` → 2025-01-15
- `%d.%m.%Y` → 15.01.2025
- `%d %B %Y` → 15 January 2025
- `%A, %d %B %Y` → Wednesday, 15 January 2025
- `%d/%m/%y` → 15/01/25

## Документация

После запуска приложения документация API доступна по адресу:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Стек технологий

- [FastAPI](https://fastapi.tiangolo.com/) — современный веб-фреймворк
- [Uvicorn](https://www.uvicorn.org/) — ASGI сервер
