from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^admin-sms$',
        'twospaces.profiles.admin.send_sms_submit',
        name="admin-send-sms"),
    url(r'^sms-sink/$',
        'twospaces.profiles.admin.sms_sink',
        name="sms_sink"),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^markdown/', include('django_markdown.urls')),
    url(r'^api/v1/token-auth$', csrf_exempt(obtain_jwt_token)),
    url('^api/', include('twospaces.urls')),
    url('^conference/', include('twospaces.conference.urls')),
]

if settings.DEBUG:
  urlpatterns += [
      url(r'^favicon.ico$',
          'pytx.views.favicon',
          name="favicon"),
      url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
          {'document_root': settings.MEDIA_ROOT}),
      url(r'^\S+/(logo\d+.png|offline.html|service-worker.js)$',
          'django.views.static.serve', {'document_root': settings.FRONT_ROOT}),
      url(r'^\S+/app-\S+?/css/pytx.css$', 'pytx.views.less_view'),
      url(r'^\S+/app-\S+?/(?P<path>.*)$', 'django.views.static.serve',
          {'document_root': settings.FRONT_ROOT}),
      url(r'^(\S+)/.*$',
          'pytx.views.index',
          name="index"),
  ]

urlpatterns += [
    url(r'^blog.rss$',
        'twospaces.blog.views.blog_rss',
        name="blog-rss"),
    url(r'^(\S+)/blog/(\S+)$',
        'pytx.views.frontend',
        name="post-detail"),
    url(r'^$',
        'pytx.views.default_conf',
        name="default-conf"),
]
