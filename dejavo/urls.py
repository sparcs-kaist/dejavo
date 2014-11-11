from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dejavo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', 'dejavo.apps.post.views.main'),
    url(r'^account/', include('dejavo.apps.account.urls')),
    url(r'^post/', include('dejavo.apps.post.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^$', 'dejavo.apps.post.views.main_redirect'),
)
