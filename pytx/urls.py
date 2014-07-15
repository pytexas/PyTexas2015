from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

from twospaces.urls import main_patterns

urlpatterns = patterns('',
  url(r'^ks/', include('pizza.kitchen_sink.urls', namespace='kitchen_sink', app_name='kitchen_sink')),
  url(r'^blogs/', include('pizza.blog.urls_blogs', namespace='blog', app_name='blog')),
  
  url('^grappelli/', include('grappelli.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url('^markdown/', include( 'django_markdown.urls')),
)

urlpatterns += main_patterns

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  
urlpatterns += patterns('',
  (r'.*', 'pizza.kitchen_sink.views.page'),
)
