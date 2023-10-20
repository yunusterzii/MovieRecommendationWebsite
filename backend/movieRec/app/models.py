from django.db import models

# Create your models here.


class Rate(models.Model):
    movieID = models.IntegerField()
    value = models.IntegerField()


class Movie(models.Model):
    movieID = models.IntegerField()
