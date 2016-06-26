from django.core.files.storage import FileSystemStorage
from django.db import models
from taggit.managers import TaggableManager

from log_in.models import UserProfile
from mahBooru.common.ImageStuff import *
from mahBooru.common.ImageStuff import create_thumbnails, add_tags, save_image, hash_image
from mahBooru.common.MyImageField import MyImageField
from mahBooru.settings import *
from django.utils.html import format_html

picture_storage = FileSystemStorage(location=MEDIA_ROOT + "/images", base_url=os.path.join(MEDIA_URL, "images/"))
preview_storage = FileSystemStorage(location=MEDIA_ROOT + "/images/preview",
                                    base_url=os.path.join(MEDIA_URL, "images/preview/"))
thumbnail_storage = FileSystemStorage(location=MEDIA_ROOT + "/images/thumbnail",
                                      base_url=os.path.join(MEDIA_URL, "images/thumbnail/"))


class PictureManager(models.Manager):
	def create_picture(self, rating, src, score, tag_string, image_data, file_extension):
		picture = Picture(rating=rating, src=src, name='', score=score)

		picture.uploaded_by = UserProfile.objects.get(
			user=UserProfile.objects.get(user=UserProfile.objects.get(user__is_superuser=True))
		)
		picture.save()

		save_image(image_data, picture.file_url, str(picture.pk) + '.' + file_extension)
		create_thumbnails(picture, '.' + picture.file_url.name.split('.')[-1])
		add_tags(picture, tag_string)
		picture.md5 = hash_image(picture.file_url)
		picture.save()
		return picture


class Picture(models.Model):
	# Picture name
	name = models.CharField(max_length=256)
	# Source URL (if presented)
	src = models.URLField(default='')
	# Initial picture size
	image_width = models.PositiveIntegerField(null=True)
	image_height = models.PositiveIntegerField(null=True)
	# Initial size picture file URL
	file_url = MyImageField(storage=picture_storage, width_field='image_width', height_field='image_height')
	# Preview picture URL
	preview_url = MyImageField(storage=preview_storage)
	# Thumbnail picture URL
	thumbnail_url = MyImageField(storage=thumbnail_storage)
	# Tags
	tags = TaggableManager()
	# Pools
	pools = models.CharField(max_length=1000)  # TODO: pools.
	# Rating (s for Safe, q for Questionable, e for Explicit)
	SAFE = 's'
	QUESTIONABLE = 'q'
	EXPLICIT = 'e'
	RATING_CHOICES = (
		(SAFE, 'Safe'),
		(QUESTIONABLE, 'Questionable'),
		(EXPLICIT, 'Explicit'),
	)
	rating = models.CharField(max_length=1, choices=RATING_CHOICES)
	# Score
	score = models.IntegerField(default=0)
	# Artist TODO: should we have artist as a new field, or just tag?
	# artist = models.CharField(max_length=256)
	# Uploader
	uploaded_by = models.ForeignKey(UserProfile)
	# Upload date and time
	upload_datetime = models.DateTimeField(auto_now_add=True)
	# Picture hash
	md5 = models.CharField(max_length=32)  # TODO: decide what to do with it.

	objects = PictureManager()

	def thumbnail_tag(self):
		return format_html('<img src="{}" />', self.thumbnail_url.url)
	thumbnail_tag.short_description = 'Image preview'
	#thumbnail_tag.allow_tags = True"""

	def __unicode__(self):
		return "Picture:" + self.name

	class Meta:
		ordering = ["id"]
