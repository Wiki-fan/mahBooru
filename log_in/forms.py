from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileRegisterForm(forms.ModelForm):
	description = forms.CharField(required=False)
	userpic = forms.ImageField(label="Choose file:")  # TODO: userpic should be optional, not necessary

	class Meta:
		model = UserProfile
		fields = ('description', 'userpic')
