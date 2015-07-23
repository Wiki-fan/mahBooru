from django.conf.urls import patterns, include, url
from django.contrib import admin
from booru import views

handler404 = "booru.views.handle404"
handler500 = "booru.views.handle500"

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mahBooru.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ ?', include('booru.urls')),
    url(r'^user/', include('log_in.urls')),
)
