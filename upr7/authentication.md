# Authentication

Lets say we have a User model like this one:

```
    class User(models.Model):
        name = models.CharField(max_length=255)
        password = models.CharField(max_length=255)
```

Using sessions we want to store the `user_id` of the currently authenticated user.

We can do that by providing `login/logout/register` functionality.

```
    # views.py

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


    def logout(request):
        request.session.pop('user_id', None)
        messages.success(request, 'Goodbuy.')
        return redirect('authentication:index')


    # we can also have a simple dashboard view

    def dashboard(request):
        if not request.session.get('user_id'):
            return redirect('authentication:login')

        user = User.objects.get(pk=request.session.get('user_id'))

        return render(request, 'dashboard.html', {
            'user': user
        })


    # Now create endpoints for this views

    # urls.py

    from authentication import views as auth_view

    app_name = 'authentication'

    urlpatterns = [
        url(r'^login/$', auth_view.login, name='login'),
        url(r'^logout/$', auth_view.logout, name='logout'),
        url(r'^register/$', auth_view.register, name='register'),
        url(r'^dashboard/$', auth_view.dashboard, name='dashboard'),
    ]
```

A simple templates can be something like this:

* `messages.html`
    ```
        {% if messages %}
        <ul class="messages">
            {% for message in messages %}
            <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    ```

* `register.html`
    ```
        {% include "messages.html" %}

        <form method="POST">
            {% csrf_token %}
            <input type="text" name="name" placeholder="name">
            <input type="password" name="password" placeholder="password">
            <input type="submit" value="Register">
        </form>

    ```

* `login.html`
    ```
        {% include "messages.html" %}

        <form method="POST">
            {% csrf_token %}
            <input type="text" name="name" placeholder="name">
            <input type="password" name="password" placeholder="password">
            <input type="submit" value="Login"> or <a href="{% url 'authentication:register' %}">Register</a>
        </form>
    ```


* `dashboard.html`
    ```
        {% include "messages.html" %}

        Hello {{user.name}}

        <a href="{% url 'authentication:logout' %}">Logout</a>
    ```


## Using build-in Django auth module

```
    from django.conf.urls import url
    from django.contrib.auth import views as auth_views
    from accounts.views import home, signup
    from django.views.generic import RedirectView
    from django.urls import reverse_lazy

    urlpatterns = [
        url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
        url(r'^logout/$', auth_views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),

        url(r'^signup/$', signup, name='signup'),
        url(r'^home/$', home, name='home'),   
        url(r'^$', RedirectView.as_view(url=reverse_lazy('home'), permanent=False)),

        # url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
        # url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

        # url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
        # url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        #     auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        # url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]
```

Where `home` and `singup` are defined like so:

```
    # accounts/views.py
    from django.contrib.auth import login, authenticate
    from django.contrib.auth.forms import UserCreationForm
    from django.conf import settings
    from django.shortcuts import render, redirect

    def home(request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        return render(request, 'accounts/home.html')

    def signup(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
```

And the templates which use django admin base template

* `home.html`
    ```
        {% extends "admin/base.html" %}

        {% block content %}

            <p>Welcome {{request.user}}</p>
            <p><a href="{% url 'logout' %}">Logout?</a></p>

        {% endblock %}
    ```

* `logged_out.html`
    ```
        {% extends "admin/base_site.html" %}
        {% load i18n %}

        {% block breadcrumbs %}<div class="breadcrumbs"><a href="{% url 'admin:index' %}">{% trans 'Home' %}</a></div>{% endblock %}

        {% block content %}

            <p>{% trans "Thanks for spending some quality time with the Web site today." %}</p>

            <p><a href="{% url 'login' %}">{% trans 'Log in again' %}</a></p>

        {% endblock %}
    ```

* `login.html`
    ```
        {% extends "admin/base.html" %}

        {% block content %}

            {% if form.errors %}
                <p>Your username and password didn't match. Please try again.</p>
            {% endif %}

            {% if next %}
                {% if user.is_authenticated %}
                    <p>Your account doesn't have access to this page. To proceed,
                        please login with an account that has access.</p>
                {% else %}
                    <p>Please login to see this page.</p>
                {% endif %}
            {% endif %}

            <form method="post">
                {% csrf_token %}
                {{form.as_ul}}
                <input type="submit" value="login" />
                <input type="hidden" name="next" value="{{ next }}" />
            </form>

            <p><a href="{% url 'signup' %}">Register?</a></p>

        {% endblock %}
    ```

* `signup.html`
    ```
        {% extends 'admin/base.html' %}

        {% block content %}
          <h2>Sign up</h2>
          <form method="post">
            {% csrf_token %}
            {{ form.as_ul }}
            <button type="submit">Sign up</button>
          </form>
        {% endblock %}
    ```