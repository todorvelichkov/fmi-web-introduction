# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.http import QueryDict
from django.urls import reverse
from django.core.exceptions import ValidationError

class Person(models.Model):
	name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
