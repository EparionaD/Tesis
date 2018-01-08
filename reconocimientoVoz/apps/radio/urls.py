from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^radio/$', views.IndexRadio.as_view(), name = 'radioindex')
]