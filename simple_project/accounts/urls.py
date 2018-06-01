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
]