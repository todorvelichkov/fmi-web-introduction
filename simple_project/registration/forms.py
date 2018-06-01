from django import forms
from registration.models import Person
from hashlib import sha1

class RegisterForm(forms.Form):
	name = forms.CharField(max_length=255)
	password1 = forms.CharField(max_length=255, widget=forms.PasswordInput)
	password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)

	def clean(self):
		super(RegisterForm, self).clean()

		name = self.cleaned_data['name']
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if Person.objects.filter(name=name).exists():
			raise forms.ValidationError({'name': 'already in use'})
		
		if not password1 == password2:
			raise forms.ValidationError({'password2': 'missmatch'})
	

class LoginForm(forms.Form):
	name = forms.CharField(max_length=255)
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)

	def clean(self):
		super(LoginForm, self).clean()
		name = self.cleaned_data['name']
		password = self.cleaned_data['password']
		pass_sha = sha1(password).hexdigest()
		if not Person.objects.filter(name=name, password=pass_sha).exists():
			raise forms.ValidationError('Invalid Credentials')
