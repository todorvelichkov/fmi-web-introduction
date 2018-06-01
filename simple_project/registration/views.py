from django.contrib import messages
from django.shortcuts import redirect, render
from registration.models import Person
from registration.forms import RegisterForm, LoginForm
from hashlib import sha1
def register(request):
	if request.session.get('user_id'):
		return redirect('registration:profile')

	if request.method == 'POST':
		form = RegisterForm(request.POST)
		
		if form.is_valid():
			name = form.cleaned_data['name']
			password1 = form.cleaned_data['password1']
			pass_hash = sha1(password1).hexdigest()
			person = Person.objects.create(name=name, password=pass_hash)
			messages.success(request, 'Welcome')
			request.session['user_id'] = person.id
			return redirect('registration:profile')
	else:
		form = RegisterForm()
				
	return render(request, 'registration/register.html', {
		'form': form
	})


def login(request):
	if request.session.get('user_id'):
		return redirect('registration:profile')

	if request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			person = Person.objects.get(name=form.cleaned_data['name'])
			messages.success(request, 'Login successfully')
			request.session['user_id'] = person.id
			return redirect('registration:profile')
	else:
		form = LoginForm()

	return render(request, 'registration/login.html', {
		'form': form
	})


def logout(request):
	request.session.pop('user_id')
	return redirect('registration:login') 


def profile(request):
	from django_tabulate import tabulate_qs
	print tabulate_qs(Person.objects.all(), tablefmt='psql')


	if not request.session.get('user_id'):
		return redirect('registration:login')

	user = Person.objects.get(id=request.session.get('user_id'))

	return render(request, 'registration/profile.html', {
		'user': user
	})