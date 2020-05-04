from __future__ import unicode_literals
from django.db import models
import re
# Create your models here.



class UserManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 1: # check if name has a value
            errors["first_name"] = "First name must be present"
        if len(postData['last_name']) < 1: # check if name has a value
            errors["last_name"] = "Last name must be present"
        if len(postData['email']) < 1: # check if email has value
            errors["email"] = "Email must be present"
        elif not EMAIL_REGEX.match(postData['email']):   # check if email is proper format based on regex       
            errors['email'] = "Invalid email address!"
        else:
            email_found = False
            for user in Users.objects.all():
                if user.email == postData['email']:
                    email_found = True
            if email_found == True:
                errors['email'] = "Email address already registered"
        if len(postData['password']) < 8: # check if password has at least 8 characters
            errors["password"] = "Password should be at least 8 characters"

        if postData['verf_password'] != postData['password']: # check if password matches 
            errors['verf_password'] = 'Passwords does not match'
        return errors

class JobManager(models.Manager):

    def basic_validator(self,postData):
        errors = {}
        if len(postData['title']) == 0:
            errors["title"] = "Title must be present"
        elif len(postData['title']) < 3: # check if name has a value
            errors["title"] = "Title must have at least 3 characters"
        if len(postData['desc']) == 0:
            errors["desc"] = "Description must be present"
        elif len(postData['desc']) < 3: # check if name has a value
            errors["desc"] = "Description have at least 3 characters"
        if len(postData['location']) == 0:
            errors["location"] = "Location must be present"
        elif len(postData['location']) < 3: # check if capacity is greater than 0
            errors["location"] = "Location have at least 3 characters"
        return errors

# class User_Category_Manager(models.Manager):
#     def basic_validator(self,PostData):
#         errors = {}
#         if 

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class User_Category(models.Model):
    category = models.CharField(max_length = 255)
    User = models.ForeignKey(Users, related_name="Category", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class Jobs(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    location =  models.CharField(max_length = 255)
    category = models.ManyToManyField(User_Category, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    created_by =  models.ForeignKey(Users, related_name="jobs_created", on_delete = models.CASCADE)
    assigned_to =  models.ForeignKey(Users, related_name="jobs_assigned", on_delete = models.CASCADE,null = True)
    objects = JobManager()