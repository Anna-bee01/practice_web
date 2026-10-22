# Берем официальный Python (как в примере)
FROM python:3.11-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Отключаем буферизацию логов (чтобы видеть print() сразу)
ENV PYTHONUNBUFFERED=1

# Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь наш код (main.py) внутрь контейнера
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска (вместо app.py запускаем uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]