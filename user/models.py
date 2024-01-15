from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#creating a class that inherits from models and has the parameters that will exist in our profile page
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete= models.CASCADE, null = True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=13,null=True)
    image = models.ImageField(default='profile.png',upload_to='Profile_images')

    def __str__(self):
        return f'{self.staff.username}-Profile'
