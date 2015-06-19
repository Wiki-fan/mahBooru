import urllib2
import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from mahBooru.settings import *


picture_storage = FileSystemStorage(location=MEDIA_ROOT+"/images", base_url=os.path.join(MEDIA_URL,"images/"))
preview_storage = FileSystemStorage(location=MEDIA_ROOT+"/images/preview", base_url=os.path.join(MEDIA_URL,"images/preview/"))
thumbnail_storage = FileSystemStorage(location=MEDIA_ROOT+"/images/thumbnail", base_url=os.path.join(MEDIA_URL,"images/thumbnail/"))


class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	description = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.user.username


class MyImageField(models.ImageField):
	def generate_filename(self, instance, filename):
		return os.path.join(self.get_directory_name(), str(instance.ID)+'.'+filename.split('.')[-1])
	
	def __unicode__(self):
		return "Image: "+self.name


class Picture(models.Model):
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=256)
	#src = models.CharField(max_length=256)
	file_url = MyImageField(storage=picture_storage)
	preview_url = MyImageField(storage=preview_storage)
	thumbnail_url = MyImageField(storage=thumbnail_storage)
	tags = TaggableManager()
	uploaded_by = models.OneToOneField(UserProfile)
	upload_datetime = models.DateTimeField(auto_now_add=True)
	
	#TODO: load from URL
	#not working
	"""def save(self, *args, **kwargs):
		filename = str(self.ID)+'.'+self.src.split('.')[-1]
		self.file_url = picture_storage.save(filename, urlopen(self.src).read())"""
	def __unicode__(self):
		return "Picture:"+self.name
		
	class Meta:
		ordering = ["ID"]

