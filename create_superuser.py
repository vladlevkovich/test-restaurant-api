import os

# Django imports
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from src.users.models import User


def create_superuser():
    email = os.getenv('SUPERUSER_EMAIL', 'admin@gmail.com')
    password = os.getenv('SUPERUSER_PASSWORD', 'admin123')
    first_name = os.getenv('SUPERUSER_FIRST_NAME', 'Admin')
    last_name = os.getenv('SUPERUSER_LAST_NAME', 'User')
    
    # Перевіряємо чи існує суперкористувач
    if not User.objects.filter(is_superuser=True).exists():
        try:
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        except Exception as e:
            print(f'Error creating superuser: {e}')
    else:
        print('Superuser already exists')

if __name__ == '__main__':
    create_superuser() 