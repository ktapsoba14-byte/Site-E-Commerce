from django.contrib import admin
from users.models import ContactMessage, Users

admin.site.register(Users)
admin.site.register(ContactMessage)
