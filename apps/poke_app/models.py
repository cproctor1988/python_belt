# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or not postData['name']:
            errors["name"] = "Name should be more than one alphabetical character."
        if len(postData['email']) < 2 or not postData['email']:
            errors["email"] = "email should be more than one alphabetical character."
        if len(postData['password']) < 8 or not postData['password']:
            errors["password"] = "password should be more than 8 alphabetical character."
        if postData['password'] != postData['passconf']:
            errors["passwordmatch"] = "Passwords do not match!."
        return errors
    def login_validator(self,postData):
        errors = {}
        user =  User.objects.get(email = postData["email"])
        if len(User.objects.filter(email = postData["email"])) < 1:
            errors['emailnotexists'] = 'Email does not exist!'
        return errors

class User(models.Model):
    name= models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 60)
    dob = models.DateField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User: {} {}".format(self.name, self.id)
class Poke(models.Model):
    poker = models.ForeignKey(User, related_name='poker')
    poked = models.ForeignKey(User, related_name='poked')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)