from django.conf.urls import url

from calc.views import calc

urlpatterns = [
    url(r'^$', calc),
]