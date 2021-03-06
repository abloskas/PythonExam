from __future__ import unicode_literals

from django.db import models
import bcrypt, md5, re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if len(postData['fname']) < 2:
            errors["fname"] = "Your name should be more than 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Your last name should be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email'  
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = 'Username already exists' 
        if len(postData['bday']) == 0: 
            errors['bday'] = "Please enter a valid birthday"
        if postData['bday'] > timestamp:
            errors['bday'] = "You must enter a date in the past"         
        if len(postData['password']) < 8:
            errors['password'] = 'Password needs to be longer than 8 characters' 
        if postData['password'] != postData['password2']:
            errors['pword'] = 'Passwords do not match'
        return errors 

    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email' 
        users = User.objects.filter(email=postData['email'])
        if len(users) == 0:
            errors['user'] = 'You are not a user. Please register'
        if len(users) != 0:
            password = users[0].password
            if bcrypt.checkpw(postData['password'].encode(), password.encode()) != True:
                errors['pword'] = "Incorrect Password. Please enter correct password"
        return errors        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __str__ (self):
        return "<User object: {} {} {} {} {}>".format(self.id, self.first_name, self.last_name, self.email, self.password)

# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)    
#     def __str__ (self):
#         return "<User object: {} {}>".format(self.name, self.users)

class Wishlist(models.Model):
    name = models.CharField(max_length=255)
    users = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    def __str__ (self):
        return "<Wishlist object: {} {}>".format(self.name, self.user)

