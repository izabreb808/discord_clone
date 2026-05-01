#!/usr/bin/env bash
set -o errexit

python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); accounts=[('Izabela','izabela@example.com','Admin12345','admin',True,True),('Pawel','pawel@example.com','Moderator12345','mod',False,False),('Karol','karol@example.com','User12345','user',False,False),('Anna','anna@example.com','User12345','user',False,False)]; [((lambda u, created, password, role, staff, superuser: (setattr(u,'role',role), setattr(u,'is_staff',staff), setattr(u,'is_superuser',superuser), u.set_password(password) if created else None, u.save()))(*User.objects.get_or_create(username=username, defaults={'email': email}), password, role, staff, superuser)) for username, email, password, role, staff, superuser in accounts]"
gunicorn discord_clone.wsgi:application --bind 0.0.0.0:${PORT:-8000}
