import re

from django.conf import settings

from pizza.blog.models import Blog

def global_vars (request):
  post = None
  
  if re.search('^/\d+/$', request.path):
    blog = Blog.objects.get(slug="main")
    if blog.published().count() > 0:
      post = blog.published()[0]
      
  context = {
    'DEV': settings.DEBUG,
    'LATEST_POST': post
  }
  
  return context
  