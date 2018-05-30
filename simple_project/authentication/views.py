# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from authentication.models import User

def index(request):
	request.session.setdefault('visits', 0)
	request.session['visits'] += 1
	return render(request, 'index.html', {
		'visits': request.session['visits']
	})

def dashboard(request):
	if not request.session.get('user_id'):
		return redirect('authentication:login')

	user = User.objects.get(pk=request.session.get('user_id'))

	return render(request, 'dashboard.html', {
		'user': user
	})


def login(request):
	if request.session.get('user_id'):
		return redirect('authentication:dashboard')

	if request.method == 'POST':
		name = request.POST['name']
		password = request.POST['password']

		try:
			user = User.objects.get(name=name, password=password)
			request.session['user_id'] = user.pk
			messages.success(request, 'Welcome back.')
			return redirect('authentication:dashboard')
		except User.DoesNotExist:
			messages.error(request, 'Invalid Credentials.')

	return render(request, 'login.html', {})

def register(request):
	if request.session.get('user_id'):
		return redirect('authentication:dashboard')

	if request.method == 'POST':
		name = request.POST['name']
		password = request.POST['password']

		if User.objects.filter(name=name).exists():
			messages.error(request, 'Name already in use.')
		else:
			user = User.objects.create(name=name, password=password)
			request.session['user_id'] = user.pk
			messages.success(request, 'Welcome.')
			return redirect('authentication:dashboard')

	return render(request, 'register.html', {})

def logout(request):
	request.session.pop('user_id', None)
	messages.success(request, 'Goodbuy.')
	return redirect('authentication:index')