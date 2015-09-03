import os
import subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from pytx.utils import index_generator
from pytx.js import SCRIPTS


class Command(BaseCommand):
  help = 'Builds front-end app'

  def add_arguments(self, parser):
    parser.add_argument('conf_slug', type=str)

  def handle(self, *args, **options):
    slug = options['conf_slug']

    os.chdir(settings.BASE_DIR)
    subprocess.call(
        'echo "RELEASE = \'"`git rev-parse --short HEAD`"\'" > release_hash.py',
        shell=True)

    from release import release
    rel = release()

    os.chdir(settings.FRONT_ROOT)

    dirs = []
    files = []
    for item in os.listdir():
      if os.path.isdir(item):
        rp = os.path.join(item, 'release.txt')
        if item != 'static' and not os.path.exists(rp):
          dirs.append(item)

      else:
        files.append(item)

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
        os.path.join(settings.FRONT_ROOT, slug, 'index.html'),)

    for index in indexes:
      fh = open(index, 'w')
      fh.write(html)
      fh.close()

    compressed = ''
    cat_cmd = 'cat '
    for s in SCRIPTS:
      with open(os.path.join(deploy_dir, s), 'r') as fh:
        compressed += fh.read() + "\n"

    cpath = os.path.join(settings.FRONT_ROOT, slug, 'app-{}'.format(rel),
                         'compressed.js')
    with open(cpath, 'w') as fh:
      fh.write(compressed)

    for file in ('logo144.png', 'offline.html', 'manifest.json'):
      cp = os.path.join(settings.FRONT_ROOT, slug, file)
      subprocess.call("cp -v {} {}".format(file, cp), shell=True)

    gen_path = os.path.join(deploy_dir, 'generated')
    subprocess.call("date > {}".format(gen_path), shell=True)

    release_path = os.path.join(settings.FRONT_ROOT, slug, 'release.txt')
    subprocess.call("echo '{}' > {}".format(rel, release_path), shell=True)
