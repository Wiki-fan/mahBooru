from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

from mahBooru.common.MyImageField import MyImageField
from mahBooru.settings import *

userpic_storage = FileSystemStorage(location=MEDIA_ROOT + "/userpics", base_url=os.path.join(MEDIA_URL, "userpics/"))


class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	description = models.CharField(max_length=256)

	userpic = MyImageField(storage=userpic_storage, default=None)

	def __unicode__(self):
		return self.user.username
