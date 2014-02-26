from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^favicon.ico$', 'pytx.views.favicon', name='favicon'),
  
  # url(r'^blog/', include('blog.urls')),
  
  url(r'^ks/', include('pizza.kitchen_sink.urls', namespace='kitchen_sink', app_name='kitchen_sink')),
  
  url('^grappelli/', include('grappelli.urls')),
  url(r'^admin/', include(admin.site.urls)),
  
  (r'.*', 'pizza.kitchen_sink.views.page'),
)
