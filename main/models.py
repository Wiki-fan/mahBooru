from django.db import models
from django.core.files.storage import FileSystemStorage
from urllib2 import *
#from django.conf import settings
from mahBooru.settings import *
import os
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

picture_storage = FileSystemStorage(location=MEDIA_ROOT+"/images", base_url=os.path.join(MEDIA_URL,"images/"))
preview_storage = FileSystemStorage(location=MEDIA_ROOT+"/images/preview", base_url=os.path.join(MEDIA_URL,"images/preview/"))
thumbnail_storage = FileSystemStorage(location=MEDIA_ROOT+"/images/thumbnail", base_url=os.path.join(MEDIA_URL,"images/thumbnail/"))

class MyImageField(models.ImageField):
	def generate_filename(self, instance, filename):
		return os.path.join(self.get_directory_name(), str(instance.ID)+'.'+filename.split('.')[-1])

class Picture(models.Model):
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=256)
	src = models.CharField(max_length=256)
	file_url = MyImageField(storage=picture_storage)
	preview_url = MyImageField(storage=preview_storage)
	thumbnail_url = MyImageField(storage=thumbnail_storage)
	tags = TaggableManager()
	
	#TODO: load from URL
	#not working
	"""def save(self, *args, **kwargs):
		filename = str(self.ID)+'.'+self.src.split('.')[-1]
		self.file_url = picture_storage.save(filename, urlopen(self.src).read())"""
	class Meta:
		ordering = ["ID"]
		
	def __unicode__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	description = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.user.username
