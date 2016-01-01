import StringIO
import hashlib
import urllib2

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from log_in.models import UserProfile
from mahBooru.settings import *
from .forms import PictureUploadForm
from .models import Picture, picture_storage


def resize_image(im, dest_size):
	image_w, image_h = im.size
	# print im.size
	aspect_ratio = image_w / float(image_h)
	new_height = int(dest_size[0] / aspect_ratio)
	new_width = int(dest_size[1] * aspect_ratio)
	# print new_height, new_width
	if new_height < dest_size[1] and new_height < image_h:
		final_width = dest_size[0]
		final_height = new_height
	elif new_width < dest_size[0] and new_width < image_w:
		final_width = new_width
		final_height = dest_size[1]
	else:
		final_width, final_height = dest_size
	# print final_width, final_height
	return im.resize((final_width, final_height), Image.ANTIALIAS)


"""def resize_image(im, dest_size):
	image_w, image_h = im.size
	aspect_ratio = image_w / float(image_h)
	if image_w<=dest_size[0]:
		return im
	else:
		final_height = int(dest_size[0] / float(image_w) * image_h)
		return im.resize((image_w, final_height), Image.ANTIALIAS)"""


@login_required(login_url='user_login')
def add_picture(request):
	context_dict = {}
	if request.method == 'POST':
		form = PictureUploadForm(request.POST, request.FILES)
		if form.is_valid():
			# Filling some fields directly from form
			instance = form.save(commit=False)
			instance.uploaded_by = UserProfile.objects.get(user=request.user)
			instance.save()

			# Uploading picture from URL
			if instance.src != '':
				filename = instance.src.split('/')[-1]
				f, e = os.path.splitext(filename)

				# TODO: need to handle unopened URLs correctly
				image_file = urllib2.urlopen(instance.src).read()
				f = str(instance.pk)
				filename = f + e
				instance.file_url.save(filename, ContentFile(image_file))
			# instance.file_url.save(instance.file_url.generate_filename(), ContentFile(image_file) )
			else:
				# Uploading picture from file
				instance.file_url = request.FILES['file_url']
				filename = instance.file_url.url.split('/')[-1]
				f, e = os.path.splitext(filename)
				f = str(instance.pk)
				filename = f + e
			# print filename, f, e

			# tags
			instance.save()
			lst = [i for i in request.POST['tags'].split(' ')]
			for i in lst:
				if i != '':
					instance.tags.add(i)

			# md5 hash
			instance.file_url.open()
			instance.md5 = hashlib.md5(instance.file_url.read()).hexdigest()
			instance.file_url.close()
			# print instance.md5

			im = Image.open(os.path.join(picture_storage.location, filename))

			# thumbnail
			thumbnail_size = (150, 150)
			o_im = resize_image(im, thumbnail_size)
			o_name = f + '.jpg'
			o_string = StringIO.StringIO()
			o_im.save(o_string, "JPEG")
			instance.thumbnail_url.save(o_name, File(o_string))
			o_string.close()

			# preview
			preview_size = (1000, 1000)
			o_im = resize_image(im, preview_size)
			o_name = f + '.jpg'
			o_string = StringIO.StringIO()
			o_im.save(o_string, "JPEG")
			instance.preview_url.save(o_name, File(o_string))
			o_string.close()

			im.close()
			o_im.close()

			instance.save()
		else:
			print form.errors
	else:
		form = PictureUploadForm()
	context_dict['picture_upload_form'] = form

	return render(request, 'booru/add_picture.html', context_dict)


def posts(request):
	context_dict = {}
	if request.method == 'GET':
		context_dict['picture'] = Picture.objects.get(id=request.GET['id'])
	# print Picture.objects.get(id=request.GET['id']).tags.names()

	return render(request, 'booru/picture.html', context_dict)


def index(request):
	context_dict = {}

	if request.method == 'GET':
		if request.GET.get('tags') is not None:
			# print request.GET.get('tags')
			query_list = [i for i in request.GET['tags'].split(' ')]
			# print query_list
			picture_list = Picture.objects.all()
			for i in query_list:
				if i != '':  # If tag is empty string
					picture_list = picture_list.filter(tags__name__contains=i).distinct()
			# picture_list = Picture.objects.filter(tags__name__contains=query_list).distinct()
			# print picture_list
		else:
			picture_list = Picture.objects.all()
		paginator = Paginator(picture_list, 18)
		page = request.GET.get('page')
		try:
			pictures = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pictures = paginator.page(1)
		except EmptyPage:  # If page is out of range, deliver last page of results.
			pictures = paginator.page(paginator.num_pages)
		context_dict['pictures'] = pictures

	return render(request, 'booru/index.html', context_dict)


def about(request):
	context_dict = {}
	return render(request, 'booru/about.html', context_dict)


def handle404(request):
	response = render_to_response("404.html", {}, context_instance=RequestContext(request))
	response.status_code = 404
	return response


def handle500(request):
	response = render_to_response("500.html", {}, context_instance=RequestContext(request))
	response.status_code = 500
	return response
