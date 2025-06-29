#!/bin/bash

# Очікуємо поки база даних буде готова
echo "Waiting for database..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
    sleep 2
done
echo "Database is ready!"

# Застосовуємо міграції
echo "Applying migrations..."
python manage.py migrate

# Створюємо суперкористувача
echo "Creating superuser..."
python create_superuser.py

# Запускаємо сервер
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 