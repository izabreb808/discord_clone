from django.contrib import admin
from .models import User, Channel, Message

admin.site.register(User)
admin.site.register(Channel)
admin.site.register(Message)