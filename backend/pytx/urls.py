from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
  url(r'^grappelli/', include('grappelli.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url('^markdown/', include( 'django_markdown.urls')),
]

if settings.DEBUG:
  urlpatterns += [
    url(r'^favicon.ico$', 'pytx.views.favicon', name="favicon"),
    url(r'^\S+/app-\S+?/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.FRONT_ROOT}),
    url(r'^(\S+)/.*$', 'pytx.views.index', name="index"),
  ]
  
urlpatterns += [
  url(r'^$', 'pytx.views.default_conf', name="default-conf"),
]