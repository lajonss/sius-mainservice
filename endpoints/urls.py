from django.conf.urls import url
from endpoints import views

urlpatterns = [
    url(r'^user/$', views.UserView.as_view()),
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.UserView.as_view()),
    url(r'^user/(?P<username>[\w.@+-]+)/(?P<appname>[\w. @+-]+)/$',
        views.UsedAppView.as_view()),
    url(r'^user/(?P<username>[\w.@+-]+)/(?P<appname>[\w. @+-]+)/$',
        views.UsedAppView.as_view()),
    url(r'^user/(?P<username>[\w.@+-]+)/(?P<appname>[\w. @+-]+)/session/$',
        views.AppSessionView.as_view()),
    url(r'^app/$', views.AppView.as_view()),
    url(r'^app/(?P<appname>[\w. @+-]+)/$', views.AppView.as_view()),
]
