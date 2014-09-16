from django.db import models

import datetime

class Person(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 passcode = models.CharField(max_length=15, blank=True, null=True)
 group_ID = models.ForeignKey('Group')
 # group = models.ForeignKey('Group')
 # ^^^ Update to this ^^^
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
 person_ID = models.ForeignKey('Person')
 # person = models.ForeignKey('Person')
 # ^^^ Update to this ^^^
 receipt_picture = models.ImageField(upload_to='receipt_pics', blank=True, null=True)
 comment = models.TextField(blank=True, null=True)

class Group(models.Model):
 name = models.CharField(max_length=200, blank=True, null=True)
 passcode = models.CharField(max_length=15, blank=True, null=True)
 person_passcodes_required = models.BooleanField(blank=True, default=False)
 use_dates = models.BooleanField(blank=True, default=False)
 use_categories = models.BooleanField(blank=True, default=False)
 use_pictures = models.BooleanField(blank=True, default=False)
 use_descriptions = models.BooleanField(blank=True, default=False)
 administrator_ID = models.ForeignKey('Person', null=True)
 deadline = models.DateField(blank=True, null=True)
 currency = models.CharField(max_length=7, default="usd")
 url_hash = models.CharField(max_length=6, null=True)
 paid = models.BooleanField(default=False)
 payment_algorithm = models.CharField(max_length=3, default="reg")

 # administrator = models.ForeignKey('Person', null=True)
 # ^^^ Update to this ^^^

 # class Meta:
 # 	verbose_name = _('user')
 # 	verbose_name_plural = _('users')

 # def get_absolute_url(self):
 # 	return "/%s/" % urlquote(self.id)

 # def get_full_name(self):
 # 	return self.name

 # def get_short_name(self):
 # 	return self.id

 # def email_user(self, subject, message, from_email=None):
 # 	# send_mail(subject, message, from_email, [self.email])



