from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import UserRegisterForm, UserProfileRegisterForm
from .models import UserProfile


def user_register(request):
	registered = False

	if request.method == 'POST':
		# Receiving register data
		user_form = UserRegisterForm(data=request.POST, files=request.FILES)
		user_profile_form = UserProfileRegisterForm(data=request.POST, files=request.FILES)
		if user_form.is_valid() and user_profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			user_profile = user_profile_form.save(commit=False)
			user_profile.user = user

			user_profile.save()

			registered = True
		else:
			print user_form.errors, user_profile_form.errors
	else:
		# Simply display form
		user_form = UserRegisterForm()
		user_profile_form = UserProfileRegisterForm()

	context_dict = {'user_form': user_form, 'user_profile_form': user_profile_form, 'registered': registered}

	return render(request, 'log_in/user_register.html', context_dict)


def user_login(request):
	context_dict = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your account is disabled")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, "log_in/user_login.html", context_dict)


@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/')


def user_profile(request):
	context_dict = {}
	if request.method == "GET":
		context_dict['usr'] = UserProfile.objects.get(user__username=request.GET.get('user'))
		# print context_dict['usr']
		return render(request, "log_in/user_profile.html", context_dict)


def user_list(request):
	context_dict = {}
	if request.method == 'GET':
		context_dict['users'] = UserProfile.objects.all()

		return render(request, "log_in/user_list.html", context_dict)
