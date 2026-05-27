from django.contrib import admin
from .models import User, Channel, DirectMessage, Message, Reaction

admin.site.register(User)
admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(DirectMessage)
admin.site.register(Reaction)
