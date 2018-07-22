from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.UserCreateView.as_view()),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.UserDeleteView.as_view()),
]