from django.conf.urls import url

from . import views

# from django.conf.urls.static import static

urlpatterns = [
	url(r'^register/$', views.user_register, name='user_register'),
	url(r'^login/$', views.user_login, name='user_login'),
	url(r'^logout/$', views.user_logout, name='user_logout'),
	url(r'^profile/$', views.user_profile, name='user_profile')
]

"""if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""
