from django.contrib import admin

# Register your models here.
from .models import Picture, UserProfile

class PictureAdmin(admin.ModelAdmin):
	list_display = ('ID', 'name', 'tags')
	
admin.site.register(Picture, PictureAdmin)
admin.site.register(UserProfile)

