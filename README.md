# Python Project: Basic Blog Website using Django and Platform.sh
This project demonstrates the ability to create a website using Django
that will be deployed to a live server (Platform.sh). Bootstrap is used for the
design elements of the website.

# Requirements
## Django:
```
$ pip install --upgrade pip
$ pip install django
```

## Bootstrap:
```
$ pip install django-bootstrap5
```
Add the following to INSTALLED_APPS in settings.py:
```
# Third party apps.
'django_bootstrap5',
```

## Platform.sh:
```
A free trial account can be created on the Platform.sh website.
```

# Notes:
Once the free trial has ended for your Platform.sh account, the blog project will
no longer be live on the website. You can still view the website locally using Django,
or you can have a paid account on Platform.sh to continue having a live website.

# Project Features:
- Users can create their own account to create, edit, and delete blog posts.
- Users can view all of their blog posts on one page, whether they are live or not.
- Admin users can review blog topics and blog posts before they are pushed live.