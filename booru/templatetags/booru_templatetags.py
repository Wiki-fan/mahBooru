from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
from taggit.models import Tag

from booru.forms import TagSearchForm

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
	updated = request.GET.copy()
	updated.update(kwargs)
	return updated.urlencode()


@register.simple_tag
def query_replace(**kwargs):
	query_dict = QueryDict('', mutable=True)
	query_dict.update(kwargs)
	return query_dict.urlencode()


@register.inclusion_tag('booru/show_all_tags.html')
def show_all_tags(request):
	paginator = Paginator(Tag.objects.all(), 20)
	tag_page = request.GET.get('tag_page')

	try:
		tags = paginator.page(tag_page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		tags = paginator.page(1)
	except EmptyPage:  # If page is out of range, deliver last page of results.
		tags = paginator.page(paginator.num_pages)
	return {'tag_paginator': tags}


@register.inclusion_tag('booru/tag_search.html')
def show_tag_search():
	return {'tag_search_form': TagSearchForm()}
