from django.conf.urls import url, include
from registration import views as reg_view

app_name = 'registration'

urlpatterns = [
    url(r'^login/$', reg_view.login, name='login'),
    url(r'^logout/$', reg_view.logout, name='logout'),
    url(r'^register/$', reg_view.register, name='register'),
    url(r'^profile/$', reg_view.profile, name='profile'),
]