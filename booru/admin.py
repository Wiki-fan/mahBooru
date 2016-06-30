from django.contrib import admin
# Register your models here.
from .models import Picture, UserProfile


class PictureAdmin(admin.ModelAdmin):
	list_display = (
		'id', 'name', 'rating', 'score', 'image_width',
		'image_height', 'thumbnail_tag'
	)
	#list_editable = ('name',)
	#fields += 'thumbnail_tag'
	#readonly_fields = ('thumbnail_tag',)

admin.site.register(Picture, PictureAdmin)
admin.site.register(UserProfile)
