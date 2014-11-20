from django.conf.urls import patterns, url

from challenges import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<challenge_id>\d+)/$', views.info, name="info"),
    url(r'^(?P<challenge_id>\d+)/edit/$', views.editChallenge, name="edit"),
    url(r'^create/$', views.createChallenge, name="create"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'challenges/login.html',
                                                         'current_app': 'challenges'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'challenges:index'}, name="logout"),
)
