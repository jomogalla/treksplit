from django.db import models

import datetime

class Person(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 passcode = models.CharField(max_length=15, blank=True, null=True)
 group_ID = models.ForeignKey('Group', on_delete=models.DO_NOTHING)
 email = models.EmailField(blank=True, null=True)
 user_login = models.CharField(max_length=30, blank=True, null=True)
 header_color = models.CharField(max_length=6)
 finalized = models.BooleanField(default=False)

class Item(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 description = models.CharField(max_length=200, blank=True, null=True)
 price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
 date = models.DateTimeField(blank=True, null=True)
 category = models.CharField(max_length=20, blank=True, null=True)
 person_ID = models.ForeignKey('Person', on_delete=models.DO_NOTHING)
 comment = models.TextField(blank=True, null=True)

class Group(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 passcode = models.CharField(max_length=15, blank=True, null=True)
 person_passcodes_required = models.BooleanField(blank=True, default=False)
 use_dates = models.BooleanField(blank=True, default=False)
 use_categories = models.BooleanField(blank=True, default=False)
 use_pictures = models.BooleanField(blank=True, default=False)
 use_descriptions = models.BooleanField(blank=True, default=False)
 administrator_ID = models.ForeignKey('Person', null=True, on_delete=models.DO_NOTHING)
 deadline = models.DateField(blank=True, null=True)
 currency = models.CharField(max_length=7, default="usd")
 url_hash = models.CharField(max_length=6, null=True)
 paid = models.BooleanField(default=False)
 payment_algorithm = models.CharField(max_length=3, default="reg")