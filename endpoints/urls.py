from django.conf.urls import url
from endpoints import views

urlpatterns = [
    url(r'^user/$', views.UserView.as_view()),
    url(r'^user/(?P<username>[^\s]+)/$', views.UserView.as_view()),
    url(r'^user/(?P<username>[^\s]+)/(?P<appname>[^\s]+)/$',
        views.UsedAppView.as_view()),
    url(r'^user/(?P<username>[^\s]+)/(?P<appname>[^\s]+)/$',
        views.UsedAppView.as_view()),
    url(r'^user/(?P<username>[^\s]+)/(?P<appname>[^\s]+)/session/$',
        views.AppSessionView.as_view()),
    url(r'^app/$', views.AppView.as_view()),
    url(r'^app/(?P<appname>[^\s]+)/$', views.AppView.as_view()),
]
