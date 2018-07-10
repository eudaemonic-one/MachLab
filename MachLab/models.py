from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from MachLab.public import model_type_choices, model_file_choices

class Userinfo(models.Model):
    user = models.OneToOneField(User)
    bio = models.CharField(max_length=256, blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=32, blank=True, null=True)
    avatar = models.FileField(upload_to='avatar/', blank=True, null=True)
    register_datetime = models.DateField(auto_now_add=True)

    #def __str__(self):
    #    return
    
class Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=32)
    model_type = models.IntegerField(choices=model_type_choices, default=(0, 'default'), blank=True)
    description = models.TextField(max_length=256, blank=True, null=True)
    star_count = models.IntegerField(default=0)
    modified_datetime = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ['-star_count']

    def __str__(self):
        return self.model_name
    
class Modelfile(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    filename = models.CharField(max_length=32)
    file = models.FileField(upload_to='models/')
    description = models.TextField(max_length=256, blank=True, null=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['-modified_datetime']

class ModelResult(Modelfile):
    result_type = models.IntegerField(choices=model_file_choices, default=(0, 'default'))

class ModelCommit(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=256, blank=True, null=True)
    commit_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-commit_datetime']
        
    def __str__(self):
        return self.description
    
class ModelPush(ModelCommit):
    push_name = models.CharField(max_length=32)

    def __str__(self):
        return self.push_name
    
class ModelPull(ModelCommit):
    def __str__(self):
        return self.description
    
class ModelDrop(ModelCommit):
    def __str__(self):
        return self.description
    
class Comment(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=256)
    comment_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)
 
class Star(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starred_datetime = models.DateTimeField(auto_now_add=True)

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
  