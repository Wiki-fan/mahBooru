import io
import hashlib

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile


# Rescales image to fit into dest_size. Does not upscale.
def resize_image(im, dest_size):
	dest_w, dest_h = dest_size
	image_w, image_h = im.size
	aspect_ratio = image_w / float(image_h)
	final_w, final_h = image_w, image_h
	if final_h > dest_h:
		final_w = int(dest_h * aspect_ratio)
		final_h = dest_h
	if final_w > dest_w:
		final_h = int(dest_w / aspect_ratio)
		final_w = dest_w
	# print final_w, final_h
	ret = None
	try:
		ret = im.resize((final_w, final_h), Image.ANTIALIAS)
	except:
		print ("Image resizing error... skip...")
	return ret


def create_thumbnails(instance, name, file_extension):
	im = Image.open(instance.file_url.path)

	# thumbnail
	thumbnail_size = (150, 150)
	o_im = resize_image(im, thumbnail_size)
	o_name = name + '.jpg'
	o_string = io.BytesIO()
	o_im.convert('RGB').save(o_string, "JPEG")
	instance.thumbnail_url.save(o_name, File(o_string))
	o_string.close()

	# preview
	preview_size = (1000, 1000)
	o_im = resize_image(im, preview_size)
	o_name = name + '.jpg'
	o_string = io.BytesIO()
	o_im.convert('RGB').save(o_string, "JPEG")
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
