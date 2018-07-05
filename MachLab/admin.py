from django.contrib.auth.models import User

user=User.objects.create_superuser('cr','cr@machlab.com','password')
user=User.objects.create_superuser('yjg','yjg@machlab.com','password')
user=User.objects.create_superuser('hhy','hhy@machlab.com','password')
user=User.objects.create_superuser('syb','syb@machlab.com','password')
