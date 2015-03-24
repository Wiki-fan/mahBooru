from django import forms
from main.models import Picture, UserProfile
from django.contrib.auth.models import User

class PictureUploadForm(forms.ModelForm):
	name = forms.CharField(label="Enter picture name:")
	#src = forms.CharField(max_length=256, help_text="Enter source URL")
	file_url = forms.ImageField(label="Choose file:")
	tags = forms.CharField(label="Enter tags, separated with whitespaces:")

	class Meta:
		model = Picture
		fields = ('name',)


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
	search_query = forms.CharField(label='Search')
	
	
