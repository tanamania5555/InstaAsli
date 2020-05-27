from django.db import models

# Create your models here.


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=300)
    clickbait = models.FloatField(default=0.0)
    def __str__(self):
        return self.link


class User(models.Model):
    id = models.AutoField(primary_key=True)
    handle = models.CharField(max_length=300)
    clickbait = models.FloatField(default=0.0)
    def __str__(self):
        return self.handle