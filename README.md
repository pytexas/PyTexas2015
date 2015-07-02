# PyTexas Website

## Setting up for development.

Requirements:

- python3
- pip3
- git
- bower (npm)
- less (npm)
- postgres db

### Requirements Installation

For any *nix platform, you'll need to edit your `/etc/hosts` and add
"db.internal" to the line starting with "127.0.0.1". It should now look like
this (unless you've made other changes to that line):

`127.0.0.1       localhost db.internal`

#### Ubuntu

```
sudo apt-get install libpq-dev python3-dev python3-pip python3-setuptools libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk nodejs npm
sudo npm install -g bower

#db
sudo apt-get install postgresql postgresql-contrib

#edit: /etc/postgresql/9.3/main/pg_hba.conf
#line: host   all   all   127.0.0.1/32   trust
#change end to "trust"
sudo -i -u postgres
createdb pytexasweb3
exit
sudo /etc/init.d/postgresql restart
```

#### OS X

These instructions assume you're using [Homebrew](http://brew.sh/). And also
that you're a slacker like me who hasn't installed Python 3.x yet.

```
# Install requirements
brew update
brew install python3  # also installs pip3
brew install npm
npm install -g bower

# Set up a virtualenv. Not strictly required, but helps preserve sanity.
# May need to do some setup for virtualenvwrapper.
sudo pip3 install virtualenvwrapper
mkvirtualenv --python=/usr/local/bin/python3 PyTexasWeb
```

For Postgres, I use [Postgres.app](http://postgresapp.com/). Regardless of what
you use, you'll need a DB called `pytexasweb3` and a user called `postgres`.
(Postgres.app uses your username on the host as a default user, so you'll likely
need to add the user.) In `psql` you can just do:

```
CREATE USER postgres CREATEDB;
CREATE DATABASE pytexasweb3;
```

## Site Installation

If you're using `virtualenv`, make sure it's activated before proceeding.

```
git clone git@github.com:pytexas/PyTexasWeb.git
git clone git@github.com:pizzapanther/TwoSpaces.git
cd PyTexasWeb/backend/
ln -s ../../TwoSpaces/twospaces/
cd ..
pip3 install -r requirements.txt
cd frontend
bower install
cd ../backend/
cp pytx/settings/local.py.example pytx/settings/local.py
# adjust local.py for your dev db if you didn't modify your hosts file
./manage.py migrate
./manage.py runserver
```

NARF