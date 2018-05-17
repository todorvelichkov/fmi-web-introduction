from django.conf.urls import url
from django.contrib.auth import views
from accounts.views import home, signup
from django.views.generic import RedirectView
from django.urls import reverse_lazy


urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),

    url(r'^signup/$', signup, name='signup'),
    url(r'^home/$', home, name='home'),   
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'), permanent=False)),

    # url(r'^password_change/$', views.PasswordChangeView.as_view(), name='password_change'),
    # url(r'^password_change/done/$', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    # url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]