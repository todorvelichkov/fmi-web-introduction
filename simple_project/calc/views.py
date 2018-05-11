# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def calc(request):

	if request.method == 'POST':
		filters = request.POST.copy()

		x = int(filters.get('x', 0))
		y = int(filters.get('y', 0))
		operation = {
			'add': lambda x,y: x+y,
			'substract': lambda x, y: x-y,
		}.get(filters.get('operation', 'add'))

		result = operation(x,y)

		filters['result'] = result

		return HttpResponseRedirect(request.path+'?'+filters.urlencode())

	filters = request.GET.copy()
	filters.setdefault('x', '0')
	filters.setdefault('y', '0')
	filters.setdefault('operation', 'add')

	return render(request, 'calc/calc_index.html', {
		'filters': filters,
	})