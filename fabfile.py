import os
import sys

from fabric.api import (run, sudo, cd, lcd, hosts, settings as fabric_settings)
from fabric.operations import get, prompt, local
from fabric.contrib.project import rsync_project

WEB_USER = "www"
WEB_HOST = 'web3.pytexas.org'


@hosts(WEB_HOST)
def deploy(slug):
  with cd('/home/www/PyTexasWeb/'):
    sudo('git pull', user=WEB_USER)
    sudo('su -c "pip3 install -r requirements.txt --user" {}'.format(WEB_USER))

  with cd('/home/www/TwoSpaces/'):
    sudo('git pull', user=WEB_USER)

  with cd('/home/www/PyTexasWeb/frontend/'):
    sudo('su -c "bower install" {}'.format(WEB_USER))

  with cd('/home/www/PyTexasWeb/backend/'):
    sudo('su -c "python3 manage.py migrate" {}'.format(WEB_USER))
    sudo('su -c "python3 manage.py collectstatic --noinput" {}'.format(
        WEB_USER))
    sudo('su -c "python3 manage.py build {}" {}'.format(slug, WEB_USER))

  sudo('supervisorctl restart pytxweb')


def deploy_local(slug):
  with lcd('/home/www/PyTexasWeb/'):
    local('git pull')
    local('pip3 install -r requirements.txt --user')

  with lcd('/home/www/TwoSpaces/'):
    local('git pull')

  with lcd('/home/www/PyTexasWeb/frontend/'):
    local('bower install --config.interactive=false')

  with lcd('/home/www/PyTexasWeb/backend/'):
    local('python3 manage.py migrate')
    local('python3 manage.py collectstatic --noinput')
    local('python3 manage.py build {}'.format(slug))

  local('supervisorctl restart pytxweb')
