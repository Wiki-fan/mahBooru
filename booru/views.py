from datetime import datetime
import os
import StringIO
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File
from django.contrib.auth.decorators import login_required
from PIL import Image
from .models import Picture, picture_storage, preview_storage, thumbnail_storage
from log_in.models import UserProfile
from .forms import PictureUploadForm, TagSearchForm
from mahBooru.settings import *

    
def resize_image(im, dest_size):
	image_w, image_h = im.size
	aspect_ratio = image_w / float(image_h)
	new_height = int(dest_size[0] / aspect_ratio)
	new_width = int(dest_size[1] * aspect_ratio)
	if new_height < dest_size[1] and new_height<image_h:
		final_width = dest_size[0]
		final_height = new_height
	elif new_width<dest_size[0] and new_width<image_w:
		final_width = new_width
		final_height = dest_size[1]
	else:
		final_width = image_w
		final_height = image_h
	return im.resize((final_width, final_height), Image.ANTIALIAS)
    
"""def resize_image(im, dest_size):
	image_w, image_h = im.size
	aspect_ratio = image_w / float(image_h)
	if image_w<=dest_size[0]:
		return im
	else:
		final_height = int(dest_size[0] / float(image_w) * image_h)
		return im.resize((image_w, final_height), Image.ANTIALIAS)"""
	
	
@login_required
def add_picture(request):
	if request.method == 'POST':
		form = PictureUploadForm(request.POST, request.FILES)

		if form.is_valid():
			instance = Picture(name=request.POST['name'])
			instance.uploaded_by = UserProfile.objects.get(user=request.user)
			instance.save()
			
			instance.file_url = request.FILES['file_url']
			lst = [i for i in request.POST['tags'].split(' ')]
			for i in lst:
				instance.tags.add(i)
			instance.save()
			
			filename = instance.file_url.url.split('/')[-1]
			f, e = os.path.splitext(filename)

			im = Image.open( os.path.join(picture_storage.location, filename)  )
			
			thumbnail_size = (150,150)
			o_im = resize_image(im, thumbnail_size)
			
			o_name = f+'.thumbnail'
			o_string = StringIO.StringIO()
			o_im.save(o_string, "JPEG")
			instance.thumbnail_url.save(o_name, File(o_string))
			o_string.close()
			
			preview_size = (1000,1000)
			o_im = resize_image(im, preview_size)
			
			o_name = f+'.jpg'
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
	context_dict = {'picture_upload_form':form}

	return render(request, 'booru/add_picture.html', context_dict)


def posts(request):
	if request.method == 'GET':
		context_dict = { 'picture': Picture.objects.get(ID=request.GET['id'])}
		#print Picture.objects.get(ID=request.GET['id']).tags.names()
	
	return render(request, 'booru/picture.html', context_dict)


def index(request):
	context_dict = {} 
	if request.method == 'GET':
		if not request.GET.get('tags') is None:
			#print request.GET.get('tags')
			query_list = [i for i in request.GET['tags'].split(' ')] 
			#print query_list
			picture_list = Picture.objects.all()
			for i in query_list:
				picture_list = picture_list.filter(tags__name__contains=i).distinct()
			#print picture_list
		else:
			picture_list = Picture.objects.all()
		context_dict['pictures'] = picture_list

	response = render(request, 'booru/index.html', context_dict)
	return response


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
