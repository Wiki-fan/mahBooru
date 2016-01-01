import urllib2

from django import forms

from .models import Picture


class PictureUploadForm(forms.ModelForm):
	name = forms.CharField(label="Picture name:", required=False)
	src = forms.CharField(max_length=256, label="Source URL", required=False)
	file_url = forms.ImageField(label="Source file", required=False)
	tags = forms.CharField(label="Tags (separated with whitespaces):", required=False)
	rating = forms.Select(choices=('s', 'q', 'e'))

	def clean(self):
		cleaned_data = super(PictureUploadForm, self).clean()
		src = cleaned_data.get('src')
		file_url = cleaned_data.get('file_url')

		if src == '' and file_url is None:
			raise forms.ValidationError('At least one of the Source and File fields should not be empty',
			                            code='no_source')
		if src != '' and file_url is not None:
			raise forms.ValidationError('You should specify only one source for the picture', code='two_sources')
		if src != '' and urllib2.urlopen(src) is None:
			raise forms.ValidationError("Can't access %(src)s", params={'src': src},
			                            code='cant_access')

	class Meta:
		model = Picture
		fields = ('name', 'rating', 'src')


class TagSearchForm(forms.Form):
	tags = forms.CharField(label='Search')
