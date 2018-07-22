from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.UserCreateView.as_view(), name="create-user"),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.UserDeleteView.as_view(), name="delete-user"),
    url(r'^(?P<pk>[0-9]+)/update/$', views.UserUpdateView.as_view(), name="update-user"),
]