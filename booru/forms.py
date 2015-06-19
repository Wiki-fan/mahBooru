from django import forms
from django.contrib.auth.models import User
from .models import Picture, UserProfile


class PictureUploadForm(forms.ModelForm):
	name = forms.CharField(label="Enter picture name:", required=False)
	#src = forms.CharField(max_length=256, help_text="Enter source URL")
	file_url = forms.ImageField(label="Choose file:")
	tags = forms.CharField(label="Enter tags, separated with whitespaces:", required=False)

	class Meta:
		model = Picture
		fields = ('name','file_url', 'tags')


class UserRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileRegisterForm(forms.ModelForm):
	description = forms.CharField(required=False)
	class Meta:
		model = UserProfile
		fields = ('description', )

		
class TagSearchForm(forms.Form):
	tags = forms.CharField(label='Search')
	
	
