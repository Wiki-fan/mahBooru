from django.conf.urls import patterns, url
from django.conf import settings
from . import views
#from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^add_picture/$', views.add_picture, name="add_picture"),
	url(r'^register/$', views.user_register, name='user_register'),
	url(r'^login/$', views.user_login, name='user_login'),
	url(r'^logout/$', views.user_logout, name='user_logout'),
	url(r'^posts$', views.posts, name='posts'),
	url(r'^about/$', views.about, name='about'),
	) 
	
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
