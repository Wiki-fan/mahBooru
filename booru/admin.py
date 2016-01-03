from django.contrib import admin
# Register your models here.
from .models import Picture, UserProfile


class PictureAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'name', 'rating', 'score', 'image_width', 'image_height', 'file_url', 'preview_url', 'thumbnail_url')


admin.site.register(Picture, PictureAdmin)
admin.site.register(UserProfile)
