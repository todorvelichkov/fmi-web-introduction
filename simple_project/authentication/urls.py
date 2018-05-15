from django.conf.urls import url

from authentication.views import index, login, logout, register, dashboard


app_name = 'authentication'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
]