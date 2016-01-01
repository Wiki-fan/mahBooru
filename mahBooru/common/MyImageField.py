import os

from django.db import models


class MyImageField(models.ImageField):
	# Generating filenames simply by object's id
	def generate_filename(self, instance, filename):
		return os.path.join(self.get_directory_name(), str(instance.pk) + '.' + filename.split('.')[-1])
