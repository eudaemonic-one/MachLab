from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=32, unique=True)
    username = models.CharField(max_length=16, unique=True) 
    password = models.CharField(max_length=16) 
    register_datetime = models.DateTimeField(auto_now_add = True)
    checkin_datetime = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.username

