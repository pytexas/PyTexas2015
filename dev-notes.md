## Development Setup

1. `git clone git@github.com:pytexas/PyTexasWeb.git`
2. `cd PyTexasWeb/`
3. `git submodule init`
4. `git submodule update`
5. `pip install -r requirements.txt`
6. `pip install -r requirements.dev.txt`
7. `cp pytx/settings/local.py.example pytx/settings/local.py`
8. Edit pytx/settings/local.py with any personal settings.
9. Setup a postgres database named **pytexasweb** at host **db.internal:5432**
10. `./manage.py syncdb`
11. `./manage.py migrate twospaces.profiles`
12. `./manage.py migrate`

**Notes:** You can also add a settings file named after your development machine in *pytx/settings/*. See *pixiebob.py* for an example.

## Deployment

**Requirements:** SSH account for pytexas.org with sudo acccess.  Talk to Paul or Glen for this.

To Deploy: `fab deploy`
