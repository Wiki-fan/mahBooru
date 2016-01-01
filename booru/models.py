from django.core.files.storage import FileSystemStorage
from django.db import models
from taggit.managers import TaggableManager

from log_in.models import UserProfile
from mahBooru.common.MyImageField import MyImageField
from mahBooru.settings import *

picture_storage = FileSystemStorage(location=MEDIA_ROOT + "/images", base_url=os.path.join(MEDIA_URL, "images/"))
preview_storage = FileSystemStorage(location=MEDIA_ROOT + "/images/preview",
                                    base_url=os.path.join(MEDIA_URL, "images/preview/"))
thumbnail_storage = FileSystemStorage(location=MEDIA_ROOT + "/images/thumbnail",
                                      base_url=os.path.join(MEDIA_URL, "images/thumbnail/"))


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

	def __unicode__(self):
		return "Picture:" + self.name

	class Meta:
		ordering = ["id"]
