from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dejavo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'dejavo.apps.zabo.views.main'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'dejavo.apps.account.views.login'),
    url(r'^logout/$', 'dejavo.apps.account.views.logout'),

    url(r'^account/', include('dejavo.apps.account.urls')),
    url(r'^article/', include('dejavo.apps.zabo.urls')),
    url(r'^manage/', include('dejavo.apps.manage.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
