from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length = 255, default = 1)


class Seeker(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    user_type = models.CharField(max_length=255,default = 1)

    def __str__(self):
        return self.name
    

class Employer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.TextField()
    user_type = models.CharField(max_length=255,default = 1)

    def __str__(self):
        return self.name
    
class ApprovedSeeker(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    user_type = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null = True,default=1)

    def __str__(self):
        return self.name
    
class ApprovedEmployer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.TextField()
    user_type = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null = True,default=1)
    

    def __str__(self):
        return self.name