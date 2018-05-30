# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
	name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
