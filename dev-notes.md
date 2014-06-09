## Development Setup

1. `git clone git@github.com:pytexas/PyTexasWeb.git`
1. `cd PyTexasWeb/`
1. `git submodule init`
1. `git submodule update`
1. `pip install -r requirements.txt`
1. `pip install -r requirements.dev.txt`
1. `cp pytx/settings/local.py.example pytx/settings/local.py`
1. Edit pytx/settings/local.py with any personal settings.
1. Setup a postgres database named **pytexasweb** at host **db.internal:5432**
1. `./manage.py syncdb`
1. `./manage.py migrate`

**Notes:** You can also add a settings file named after your development machine in *pytx/settings/*. See *pixiebob.py* for an example.

## Deployment

Coming Soon.
