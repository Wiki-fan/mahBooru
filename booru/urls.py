from django.conf.urls import url

from . import views

# from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^add_picture/$', views.add_picture, name="add_picture"),
	url(r'^posts$', views.posts, name='posts'),
	url(r'^about/$', views.about, name='about'),
]

"""if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""
