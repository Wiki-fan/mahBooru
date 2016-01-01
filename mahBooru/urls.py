from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

handler404 = "booru.views.handle404"
handler500 = "booru.views.handle500"

urlpatterns = [
	# Examples:
	# url(r'^$', 'mahBooru.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^ ?', include('booru.urls')),
	url(r'^user/', include('log_in.urls')),
	# url(r'^ ?', RedirectView.as_view(url='booru/', permanent=False), name='index'),
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
