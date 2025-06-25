# 🌱 ecopoints

****
IMPORTANT - Original commits were made under a local-only Git identity, so GitHub does not attribute them to my account. This repository is a copy to showcase my work.

## What is in environment

- python 3.7.5
- django 2.1.5
- django-compressor 4.4
- django-libsass 0.9
- django-registration-redux 2.13

## Installation

Based on the assumption anaconda is being used -
**To install the required packages, run the following commands:**

```bash
conda create --name {ENVNAME} python=3.7.5 django=2.1.5 
```

```bash
pip install django-compressor django-libsass
```

**django-registration-redux package version in the tango book doesn't seem to compatible please install this version
instead:**

```bash
pip install django-registration-redux==2.13
```

```bash
pip install django-feather
```

### Setup

Setup database:

```bash
python manage.py migrate
```

populate database:

```bash
python ./populate_ecopoints.py
```

make sure to create a superuser:

```bash
python manage.py createsuperuser
```

**If there is issues with the database, delete the db.sqlite3 file and run the following commands:**

```bash
# this will delete database; use for clean restart
rm db.sqlite3
python manage.py migrate
python ./populate_ecopoints.py
```

****

## Features

- User authentication
- Log and track sustainable actions
- Dashboard
- Analytics

****

## Created by

- Kimberley Bates
- Lily Cameron
- Alexandra Gibson
- Geraldine Ho
