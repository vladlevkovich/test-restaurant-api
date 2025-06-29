FROM python:3.11-slim

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли залежностей
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код проекту
COPY . .

# Створюємо директорію для медіа файлів
RUN mkdir -p /app/media

# Встановлюємо права доступу
RUN chmod +x /app/entrypoint.sh

# Відкриваємо порт
EXPOSE 8000

# Запускаємо entrypoint скрипт
ENTRYPOINT ["/app/entrypoint.sh"]