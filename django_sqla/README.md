How Tos:
===

1. Change django\_sqla/settings.py:  `DATABASE_ENGINE` to your own db engine string, mine looks like:  
    `DATABASE_ENGINE = "mysql://root:root@localhost/django_sqla"`

2. Create database `django_sqla`, if you change the `DATABASE_ENGINE`,  create your own database.

3. Type  
    `python manage.py runserver 0.0.0.0:8000`  
to run your server.

4. Through `ip:8000` in your browser to view the results. You may see this:  
![run server results](results.png)
