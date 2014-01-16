from django.db import models

import datetime

class Person(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 passcode = models.CharField(max_length=15, blank=True, null=True)
 group_ID = models.ForeignKey('Group')
 email = models.EmailField(blank=True, null=True)
 user_login = models.CharField(max_length=30, blank=True, null=True)
 header_color = models.CharField(max_length=6)
 #  ^^^ create a default value to be called something like: default=lambda:{"email": "to1@example.com"}

class Item(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 description = models.CharField(max_length=200, blank=True, null=True)
 price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
 date = models.DateTimeField(blank=True, null=True)
 category = models.CharField(max_length=20, blank=True, null=True)
 person_ID = models.ForeignKey('Person')
 receipt_picture = models.ImageField(upload_to='receipt_pics', blank=True, null=True)

class Group(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 passcode = models.CharField(max_length=15, blank=True, null=True)
 person_passcodes_required = models.BooleanField(blank=True, default=False)
 use_dates = models.BooleanField(blank=True, default=False)
 use_categories = models.BooleanField(blank=True, default=False)
 use_pictures = models.BooleanField(blank=True, default=False)
 use_descriptions = models.BooleanField(blank=True, default=False)
 administrator_ID = models.ForeignKey('Person', null=True)
 #add a currency field




