# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.http import QueryDict
from django.urls import reverse
from django.core.exceptions import ValidationError

class CalcResult(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    operation = models.CharField(
        max_length=20,
        choices=[
        ('add', 'Add'),
        ('substract', 'Substract'),
    ])
    result = models.FloatField()

    def get_absolute_url(self):
        q = QueryDict(mutable=True)
        pub_attrs = {k:v for k,v in self.__dict__.items() if not k.startswith('_')}
        q.update(pub_attrs)
        return  '%s?%s' % (
            reverse('calc_index'),
            q.urlencode()
        )

    def clean(self):
        self.result = self.get_result()
        # if not self.result == self.get_result():
        #     raise ValidationError({'result': 'InvalidResult'})

    def get_result(self):
        operation = {
            'add': lambda x,y: x+y,
            'substract': lambda x, y: x-y,
        }.get(self.operation)

        return operation(self.x, self.y)

    def __str__(self):
        return '<Res: %s>' % (
            self.result,
        )