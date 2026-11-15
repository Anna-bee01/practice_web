# Лабораторная работа 4. Архитектура приложения с разделением слоёв

## Описание
Рефакторинг REST API с разделением на слои (Handler / Service / Repository) и внедрением зависимостей (Dependency Injection).

## Архитектура
- `routers.py` (Handler) — принимает HTTP-запросы.
- `service.py` (Service) — бизнес-логика и правила.
- `repository.py` (Repository) — работа с данными.
- `models.py` — Pydantic-модели.
- `config.py` — конфигурация через переменные окружения.

## Как запустить
1. Убедитесь, что установлен Docker Desktop.
2. Откройте терминал в папке `lab_4`.
3. Выполните команду:
   ```bash
   docker compose up --build
4. Откройте в браузере: http://127.0.0.1:8003/docs