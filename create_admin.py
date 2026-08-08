import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "shujaa"
password = os.environ.get("DJANGO_ADMIN_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        password=password,
    )
    print("Admin user created successfully.")
else:
    print("Admin user already exists.")
