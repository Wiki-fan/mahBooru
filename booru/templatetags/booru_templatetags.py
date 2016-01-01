from django import template
from django.http import QueryDict
from taggit.models import Tag

from booru.forms import TagSearchForm

register = template.Library()


# TODO: make it cleaner and simpler.
@register.simple_tag
def query_transform(request, **kwargs):
	if request == '':
		updated = QueryDict('', mutable=True)
	else:
		updated = request.GET.copy()
	updated.update(kwargs)
	return updated.urlencode()


@register.simple_tag
def query_replace(**kwargs):
	query_dict = QueryDict('', mutable=True)
	query_dict.update(kwargs)
	return query_dict.urlencode()


@register.inclusion_tag('booru/show_all_tags.html')
def show_all_tags():
	return {'tags': Tag.objects.all()}


@register.inclusion_tag('booru/tag_search.html')
def show_tag_search():
	return {'tag_search_form': TagSearchForm()}
