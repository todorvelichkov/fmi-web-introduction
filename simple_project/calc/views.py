# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from calc.forms import CalcForm
from calc.models import CalcResult

# Create your views here.
def calc(request):
	if request.method == 'POST':
		form = CalcForm(request.POST)

		if form.is_valid():
			calc_res = form.save()

			return HttpResponseRedirect(
				calc_res.get_absolute_url()
			)
	else:
		filters = request.GET.copy()
		filters.setdefault('x', '0')
		filters.setdefault('y', '0')
		filters.setdefault('operation', 'add')
		form = CalcForm(filters)

	results = CalcResult.objects.all()
	return render(request, 'calc/calc_index.html', {
		'form': form,
		'results': results,
	})