import os
import subprocess
from string import Template

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.loader import render_to_string

class Command (BaseCommand):
  help = 'Builds front-end app'
  
  def add_arguments (self, parser):
    parser.add_argument('conf_slug', type=str)
    
  def handle (self, *args, **options):
    slug = options['conf_slug']
    
    os.chdir(settings.BASE_DIR)
    subprocess.call('echo "RELEASE = \'"`git rev-parse --short HEAD`"\'" > release_hash.py', shell=True)
    
    os.chdir(settings.FRONT_ROOT)
    
    dirs = (
      'bower',
      'controllers',
      'css',
      'img',
      'templates',
    )
    
    files = (
      'app.js',
      'favicon.ico',
    )
    
    from release import release
    
    rel = release()
    deploy_dir = os.path.join(settings.FRONT_ROOT, slug, 'app-{}'.format(rel))
    if not os.path.exists(deploy_dir):
      os.makedirs(deploy_dir)
      
    for file in files:
      subprocess.call("cp -v {} {}".format(file, deploy_dir), shell=True)
      
    for d in dirs:
      subprocess.call("cp -rv {} {}".format(d, deploy_dir), shell=True)
      
    context = dict(
      base='/{}/app-{}'.format(slug, rel),
      conf=slug,
      api_base='/',
    )
    
    template = render_to_string('prebuild-index.html', {})
    html = Template(template).safe_substitute(context)
    
    indexes = (
      os.path.join(deploy_dir, 'index.html'),
      os.path.join(settings.FRONT_ROOT, slug, 'index.html'),
    )
    
    for index in indexes:
      fh = open(index, 'w')
      fh.write(html)
      fh.close()
      