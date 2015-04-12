import os
import sys

from fabric.api import (
  run,
  sudo,
  cd,
  hosts,
  settings as fabric_settings
)
from fabric.operations import get, prompt, local
from fabric.contrib.project import rsync_project

WEB_USER = "www"
WEB_HOST = 'web3.pytexas.org'

@hosts(WEB_HOST)
def deploy (slug):
  with cd('/home/www/PyTexasWeb/'):
    sudo('git pull', user=WEB_USER)
    sudo('su -c "pip3 install -r requirements.txt --user" {}'.format(WEB_USER))
    
  with cd('/home/www/TwoSpaces/'):
    sudo('git pull', user=WEB_USER)
    
  with cd('/home/www/PyTexasWeb/backend/'):
    #sudo('su -c "python3 manage.py migrate" {}'.format(WEB_USER))
    sudo('su -c "python3 manage.py build {}" {}'.format(slug, WEB_USER))
    
  #sudo('supervisorctl restart pytx')
  