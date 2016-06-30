from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
    email = models.TextField(unique=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    password = models.TextField()

    class Meta:
        app_label = 'vanguard'


class Sessions(models.Model):
    key = models.TextField(unique=True, max_length=500)
    last_used = models.TextField(null=True)
    user = models.ForeignKey('Users', models.CASCADE)

    class Meta:
        app_label = 'vanguard'
