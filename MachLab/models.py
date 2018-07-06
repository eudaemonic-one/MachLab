from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User

class Userinfo(models.Model):
    user = models.OneToOneField(User)
    bio = models.CharField(max_length=256)
    url = models.URLField(max_length=256)
    location = models.CharField(max_length=32)
    avatar = models.FileField(upload_to='avatar/')
    register_datetime = models.DateField(auto_now_add=True)

    def get_bio(self):
        return self.bio

    def get_url(self):
        return self.url

    def get_location(self):
        return self.location
    
    def get_avatar(self):
        return self.avatar
      
    def get_registered_date(self):
        return self.registered_date
    
class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        "Creates and saves a User with the given email, date of birth and password."
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(self, username=username, email=email, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        "Creates and saves a superuser with the given email, date of birth and password."
        user = self.model(username=username, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=32, unique=True)
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    bio = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    location = models.CharField(max_length=32)
    avatar = models.FileField(upload_to='static/media/avatar/')
    register_datetime = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def get_email(self):
        return self.email
    
    def get_username(self):
        return self.username

    def get_bio(self):
        return self.bio

    def get_url(self):
        return self.url

    def get_location(self):
        return self.location
    
    def get_registered_date(self):
        return self.registered_date
    
    def get_avatar(self):
        return self.avatar
    
    def update(self, email, username, bio=None, url=None, location=None):
        if email is not None:
            self.email = email
        if username is not None:
            self.username = username
        if bio is not None:
            self.bio = bio
        if url is not None:
            self.url = url
        if location is not None:
            self.location = location

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
  