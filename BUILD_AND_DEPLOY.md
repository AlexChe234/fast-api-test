# Build and Deploy

Документация по сборке и развёртыванию приложения.

## Содержание

- [Локальная сборка](#локальная-сборка)
- [Docker сборка](#docker-сборка)
- [CI/CD](#cicd)
- [Деплой на сервер](#деплой-на-сервер)
- [Переменные окружения](#переменные-окружения)

---

## Локальная сборка

### Требования

- Python 3.11+
- pip

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск в режиме разработки

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000`

### Запуск продакшен версии

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Docker сборка

### Сборка образа

```bash
docker build -t fastapi-app .
```

### Запуск контейнера

```bash
docker run -d -p 8000:8000 --name my-app fastapi-app
```

### Проверка работающего контейнера

```bash
docker ps
docker logs my-app
```

### Остановка и удаление

```bash
docker stop my-app
docker rm my-app
```

### Сборка с кастомным тегом

```bash
docker build -t ghcr.io/username/repo:tag .
```

### Использование Docker Compose

Создайте файл `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
```

Запуск:

```bash
docker-compose up -d
```

---

## CI/CD

Проект использует GitHub Actions для автоматической сборки и деплоя.

### Workflow файл

Конфигурация: `build-and-deploy.yml`

### Триггеры

| Событие | Действие |
|---------|----------|
| Push в `main` | Сборка и деплой |
| Тег `v*` | Сборка и деплой |
| Ручной запуск | Сборка и деплой |

### Процесс CI/CD

```
1. Checkout → Скачивание кода
2. Convert to lowercase → Преобразование имени репозитория в нижний регистр
3. Setup Docker Buildx → Настройка сборки
4. Login to Container Registry → Авторизация в GHCR
5. Build and push → Сборка и пуш образа в GHCR
6. Deploy (if not PR) → Деплой на сервер через SSH
```

### Реестр образов

- Registry: `ghcr.io`
- Image name: `{owner}/{repo}` (в нижнем регистре)
- Теги: `latest`, `{sha}`

### Примеры тегов образа

| Событие | Тег |
|---------|-----|
| Push в main | `{sha}` + `latest` |
| Тег v1.0.0 | `{sha}` + `latest` |

> **Важно:** Имя репозитория автоматически преобразуется в нижний регистр (например, `AlexChe234/fast-api-test` → `alexche234/fast-api-test`).

---

## Деплой на сервер

### Требования к серверу

- Ubuntu/Debian сервер
- Docker и Docker Compose
- SSH доступ
- Настроенные secrets в GitHub

### Настройка Secrets

В репозитории GitHub перейдите в **Settings → Secrets and variables → Actions** и добавьте:

| Secret | Описание |
|--------|----------|
| `SSH_HOST` | IP адрес или hostname сервера |
| `SSH_PORT` | Порт SSH (обычно 22) |
| `SSH_USERNAME` | Имя пользователя для SSH |
| `SSH_PRIVATE_KEY` | Приватный SSH ключ |

> **Примечание:** `GHCR_TOKEN` больше не требуется — workflow использует встроенный `${{ secrets.GITHUB_TOKEN }}`.

### Настройка SSH ключа

1. Сгенерируйте ключ на сервере (если нет):
   ```bash
   ssh-keygen -t ed25519 -C "deploy@server"
   ```

2. Добавьте публичный ключ в `~/.ssh/authorized_keys`

3. Скопируйте приватный ключ в GitHub Secrets

### Ручной деплой

```bash
# Логин в registry
echo "$GITHUB_TOKEN" | docker login ghcr.io -u $USERNAME --password-stdin

# Определяем образ (имя в нижнем регистре!)
IMAGE_NAME_LOWER=$(echo "username/repo" | tr '[:upper:]' '[:lower:]')
IMAGE="ghcr.io/$IMAGE_NAME_LOWER:commit-sha"

# Останавливаем старый контейнер
docker stop my-app 2>/dev/null || true
docker rm my-app 2>/dev/null || true

# Запускаем новый
docker run -d --name my-app \
  --restart unless-stopped \
  -p 8000:8000 \
  "$IMAGE"
```

### Структура деплоя на сервере

Контейнер запускается напрямую через Docker:

```
Контейнер: my-app
Порт: 8000:8000
Restart policy: unless-stopped
```

### Мониторинг

```bash
# Просмотр логов
docker logs my-app -f

# Проверка статуса
docker ps

# Проверка использования ресурсов
docker stats my-app

# Проверка доступности приложения
curl http://localhost:8000/
```

---

## Переменные окружения

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `PYTHONUNBUFFERED` | `1` | Вывод логов без буферизации |
| `PORT` | `8000` | Порт приложения |
| `HOST` | `0.0.0.0` | Хост для прослушивания |

### Пример с переменными окружения

```bash
docker run -d \
  -p 8000:8000 \
  -e PYTHONUNBUFFERED=1 \
  --name my-app \
  fastapi-app
```

---

## Устранение проблем

### Контейнер не запускается

```bash
# Проверить логи
docker logs my-app

# Проверить статус
docker inspect my-app
```

### Ошибка авторизации в GHCR

Убедитесь, что:
1. Репозиторий имеет права `packages: write` в настройках workflow
2. Репозиторий публичный или токен имеет доступ к приватным пакетам

### Ошибка "invalid reference format: repository name must be lowercase"

Имя репозитория должно быть в нижнем регистре. Workflow автоматически преобразует имя, но при ручном деплое используйте:

```bash
IMAGE_NAME_LOWER=$(echo "$REPO_NAME" | tr '[:upper:]' '[:lower:]')
```

### Проблемы с портом

```bash
# Проверить занятые порты
netstat -tulpn | grep 8000

# Использовать другой порт
docker run -p 8080:8000 fastapi-app
```

---

## Безопасность

- Не храните secrets в коде
- Используйте GitHub Secrets для конфиденциальных данных
- Регулярно обновляйте базовый образ Python
- Ограничьте права SSH пользователя для деплоя
