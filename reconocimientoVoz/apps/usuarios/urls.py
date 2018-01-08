from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name = 'index'),
    url(r'^login/$', LoginView.as_view(template_name = 'usuarios/login.html'), name = 'login'),
    url(r'^logout/$', LogoutView.as_view(next_page = '/'), name = 'logout')
]