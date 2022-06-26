from tkinter import CASCADE
from django.db import models
import re
from django.db import models


class ShowManager(models.Manager):
    # 3rd params is the current instance
    def basic_validator(self, postData, user=None):
        # add keys and values to errors dictionary for each invalid field
        errors = {}

        # validate name ,required; at least 3 characters; letters only
        if not postData["name"]:
            errors["name"] = "Please enter your name"
        elif len(postData["name"]) < 3:
            errors["name"] = "name should be at least 3 characters"
        elif not re.match(r'^[a-zA-Z]+$', postData["name"]):
            errors["first_name"] = "name should contain letters only"

        # validate name ,required; at least 3 characters
        if not postData["username"]:
            errors["username"] = "Please enter your username"
        elif len(postData["username"]) < 3:
            errors["username"] = "username should be at least 3 characters"
        
        # validate password , required; at least 8 characters; matches password confirmation
        if not postData["password"]:
            errors["password"] = "Please enter your password"
            # string like (gr3at@3wdsG)
        elif not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', postData['password']):
            errors["password"] = "password should be strong"
        return errors


class User(models.Model):
    name = models.CharField(max_length=40)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=60)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

class Wish(models.Model):
    item_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ForeignKey(User, related_name="wishes",on_delete=CASCADE,blank=True,null=True)
    user_wishs = models.ManyToManyField(User, related_name="fav_wishes",blank=True)
    objects = ShowManager()

