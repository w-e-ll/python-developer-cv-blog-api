Python Developer CV, Blog, API
-------

Simple and really extendable Python/Django application for managing a  developer CV, blog posts, blog API within your Web based application.
Categories, tags, tag category, blog posts API with Django REST Framework JWT (JSON Web Token Authentication support), Disqus comments, contacts page, user registration, sitemap, robots.txt.
Application based on Python3.6, PostgreSQL, Django 2.0, Django Rest Framework and Bootstrap.
Fully SEO optimized content with implemented Google rich snippets, structured data.

### Online:
- [https://w-e-ll.com](https://w-e-ll.com)

### Technologies

- Django 2.0
- Python 3.6
- PostgreSQL
- Django REST Framework

### Features

- Django Suit (Modern theme for Django admin interface);
- Face 90% bootstrap;
- Django Wysiwyg Redactor (A lightweight wysiwyg editor for Django);
- Django disqus for comments;
- Admin Site: Accounts, CV, Blog (Author, Post, Page, Category, Tag, Gallery), Robots;
- Pagination posts, Display posts under tags, Display posts under Author, Sitemap page;
- Related blog posts;
- Next and previous for post;
- sitemap.xml, robots.txt;
- Contacts page;
- Json post view;
- Auto backup to the json file;
- and much more...

### Make Initial Setup:

- virtualenv -p python3.6 developer-blog
- activate it (source bin/activate)
- git clone https://github.com/w-e-ll/python-developer-cv-blog-api.git
- cd src
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

> You'll get a few errors, bacouse of django 2.0
> Need to change names of imports (from django.core.urlresolvers import reverse - change to from django.urls import reverse)
> Change names in a few functions (assignment_tag to simple tag)
-------
