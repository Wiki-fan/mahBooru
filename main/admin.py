from django.contrib import admin

# Register your models here.
from main.models import Picture, UserProfile

admin.site.register(Picture)
admin.site.register(UserProfile)

