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
    
class JobPost(models.Model):
    job_designation = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='job_images/')
    posting_date = models.DateField()
    last_date_to_apply = models.DateField()
    other_requirements = models.TextField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="pending")

    def __str__(self):
        return self.job_designation

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username