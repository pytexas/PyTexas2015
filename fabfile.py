from fabric.api import run, sudo, cd, hosts

WEB_USER = "www-data"

@hosts('pytexas.org')
def deploy ():
  with cd('/var/www/PyTexasWeb/'):
    sudo('git pull', user=WEB_USER)
    sudo('git submodule update', user=WEB_USER)
    sudo('su -c "pip install -r requirements.txt --user" {}'.format(WEB_USER))
    sudo('su -c "./manage.py migrate" {}'.format(WEB_USER))
    sudo('su -c "./manage.py collectstatic --noinput" {}'.format(WEB_USER))
    
    sudo('sudo supervisorctl restart pytx')
    