from django.db import models
#used to store the data in the database in a very specific way
#in every update of models ensure two things
#   1) app should be added in settings installed apps
#   2) python manage.py makemigrations followed by python manage.py migrate
# Create your models here.


class Devotee_detail(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique = True)
    content = models.TextField(null = True, blank= True)

#something very similar to python
# class Blog:
#     title = "Hare Krishna"
#     content = "something"