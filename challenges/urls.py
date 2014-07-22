from django.conf.urls import patterns, url

from challenges import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.InfoView.as_view(), name="info"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'challenges/login.html',
                                                         'current_app': 'challenges'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'challenges:index'}, name="logout"),
)
