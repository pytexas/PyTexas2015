from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
  url(r'^grappelli/', include('grappelli.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url('^markdown/', include( 'django_markdown.urls')),
  url('^api/', include( 'twospaces.urls')),
]

if settings.DEBUG:
  urlpatterns += [
    url(r'^favicon.ico$', 'pytx.views.favicon', name="favicon"),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
    url(r'^(logo144.png|offline.html|service-worker.js)$', 'django.views.static.serve',
      {'document_root': settings.FRONT_ROOT}),
    url(r'^\S+/app-\S+?/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.FRONT_ROOT}),
    url(r'^(\S+)/.*$', 'pytx.views.index', name="index"),
  ]
  
urlpatterns += [
  url(r'^blog.rss$', 'twospaces.blog.views.blog_rss', name="blog-rss"),
  url(r'^(\S+)/blog/(\S+)$', 'pytx.views.frontend', name="post-detail"),
  url(r'^$', 'pytx.views.default_conf', name="default-conf"),
]