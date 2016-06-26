import urllib.request, urllib.error, urllib.parse

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from log_in.models import UserProfile
from mahBooru.common.ImageStuff import create_thumbnails, add_tags, save_image, hash_image
from mahBooru.settings import *
from .forms import PictureUploadForm
from .models import Picture


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
				f = str(instance.pk)
				filename = f + e
				save_image(urllib.request.urlopen(instance.src).read(), instance.file_url, filename)
			# instance.file_url.save(instance.file_url.generate_filename(), ContentFile(image_file) )
			else:
				# Uploading picture from file
				instance.file_url = request.FILES['file_url']
				filename = instance.file_url.url.split('/')[-1]
				f, e = os.path.splitext(filename)
				f = str(instance.pk)
				filename = f + e
			# print (filename, f, e)

			# tags
			instance.save()
			add_tags(instance, request.POST['tags'])

			# md5 hash
			instance.md5 = hash_image(instance.file_url)
			# print (instance.md5)

			create_thumbnails(instance, f)

			instance.save()
		else:
			print((form.errors))
	else:
		form = PictureUploadForm()
	context_dict['picture_upload_form'] = form

	return render(request, 'booru/add_picture.html', context_dict)


def posts(request):
	context_dict = {}
	if request.method == 'GET':
		context_dict['picture'] = Picture.objects.get(id=request.GET['id'])
	# print (Picture.objects.get(id=request.GET['id']).tags.names())

	return render(request, 'booru/picture.html', context_dict)


def index(request):
	context_dict = {}

	if request.method == 'GET':
		if request.GET.get('tags') is not None:
			# print (request.GET.get('tags'))
			query_list = [i for i in request.GET['tags'].split(' ')]
			# print (query_list)
			picture_list = Picture.objects.all()
			for i in query_list:
				if i != '':  # If tag is empty string
					picture_list = picture_list.filter(tags__name__contains=i).distinct()
				# picture_list = Picture.objects.filter(tags__name__contains=query_list).distinct()
				# print (picture_list)
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
