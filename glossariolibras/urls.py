from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'glossario.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', include(admin.site.urls)),
    url(r'^(?P<glosssario>\w+)$', 'glossario.views.index', name='glossarios'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
