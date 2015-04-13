import os
import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from pytx.utils import index_generator

class Command (BaseCommand):
  help = 'Builds front-end app'
  
  def add_arguments (self, parser):
    parser.add_argument('conf_slug', type=str)
    
  def handle (self, *args, **options):
    slug = options['conf_slug']
    
    os.chdir(settings.BASE_DIR)
    subprocess.call('echo "RELEASE = \'"`git rev-parse --short HEAD`"\'" > release_hash.py', shell=True)
    
    from release import release
    rel = release()
    
    os.chdir(settings.FRONT_ROOT)
    
    dirs = (
      'bower',
      'controllers',
      'css',
      'img',
      'templates',
      'pages',
      'directives',
    )
    
    files = (
      'app.js',
      'favicon.ico',
    )
    
    deploy_dir = os.path.join(settings.FRONT_ROOT, slug, 'app-{}'.format(rel))
    if not os.path.exists(deploy_dir):
      os.makedirs(deploy_dir)
      
    for file in files:
      subprocess.call("cp -v {} {}".format(file, deploy_dir), shell=True)
      
    for d in dirs:
      subprocess.call("cp -rv {} {}".format(d, deploy_dir), shell=True)
      
    less = os.path.join(deploy_dir, 'css', 'pytx')
    subprocess.call("lessc {}.less {}.css".format(less, less), shell=True)
    
    html = index_generator(slug, dev=False)
    indexes = (
      os.path.join(deploy_dir, 'index.html'),
      os.path.join(settings.FRONT_ROOT, slug, 'index.html'),
    )
    
    for index in indexes:
      fh = open(index, 'w')
      fh.write(html)
      fh.close()
      
    gen_path = os.path.join(deploy_dir, 'generated')
    subprocess.call("date > {}".format(gen_path), shell=True)
    
    release_path = os.path.join(settings.FRONT_ROOT, slug, 'release.txt')
    subprocess.call("echo '{}' > {}".format(rel, release_path), shell=True)
    