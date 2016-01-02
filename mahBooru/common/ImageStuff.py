import StringIO
import hashlib

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile


# TODO: better rescaling.
def resize_image(im, dest_size):
	dest_w, dest_h = dest_size
	image_w, image_h = im.size
	# print im.size
	aspect_ratio = image_w / float(image_h)
	"""if image_h > dest_h:
		final_w = dest_h*aspect_ratio
		final_h = dest_h
	if image_w > dest_w:
		final_h = dest_w/aspect_ratio
		final_w = dest_w"""
	new_height = int(dest_size[0] / aspect_ratio)
	new_width = int(dest_size[1] * aspect_ratio)
	# print new_height, new_width

	if new_height < dest_size[1] and new_height < image_h:
		final_width = dest_size[0]
		final_height = new_height
	elif new_width < dest_size[0] and new_width < image_w:
		final_width = new_width
		final_height = dest_size[1]
	elif new_height > dest_size[1] and new_height < image_h:
		final_width = new_width
		final_height = image_h
	elif new_width < dest_size[0] and new_width < image_w:
		final_width = image_w
		final_height = new_height
	else:
		final_width, final_height = dest_size
	# print final_width, final_height
	return im.resize((final_width, final_height), Image.ANTIALIAS)


"""def resize_image(im, dest_size):
	image_w, image_h = im.size
	aspect_ratio = image_w / float(image_h)
	if image_w<dest_size[0]:
		return im
	else:
		final_height = int(dest_size[0] / float(image_w) * image_h)
		return im.resize((image_w, final_height), Image.ANTIALIAS)"""


# def resize_thumbnail(im, dest_size):


def create_thumbnails(instance, name):
	im = Image.open(instance.file_url.path)

	# thumbnail
	thumbnail_size = (150, 150)
	o_im = resize_image(im, thumbnail_size)
	o_name = name + '.jpg'
	o_string = StringIO.StringIO()
	o_im.save(o_string, "JPEG")
	instance.thumbnail_url.save(o_name, File(o_string))
	o_string.close()

	# preview
	preview_size = (1000, 1000)
	o_im = resize_image(im, preview_size)
	o_name = name + '.jpg'
	o_string = StringIO.StringIO()
	o_im.save(o_string, "JPEG")
	instance.preview_url.save(o_name, File(o_string))
	o_string.close()

	im.close()
	o_im.close()


def add_tags(instance, tag_string):
	lst = [i for i in tag_string.split(' ')]
	for i in lst:
		if i != '':
			instance.tags.add(i)


def save_image(image_data, file_field, filename):
	file_field.save(filename, ContentFile(image_data))


def hash_image(file_url):
	file_url.open()
	hash = hashlib.md5(file_url.read()).hexdigest()
	file_url.close()
	return hash
