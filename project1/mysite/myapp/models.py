from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username