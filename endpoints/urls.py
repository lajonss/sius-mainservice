from django.conf.urls import url
from endpoints import views

urlpatterns = [
    url(r'^user/(?P<username>[A-Za-z_\-0-9]+)/$', views.UserView.as_view()),
]
