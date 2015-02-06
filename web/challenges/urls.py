from django.conf.urls import patterns, url

from challenges import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^ranking/$', views.ranking, name="ranking"),
    url(r'^challenge/(?P<challenge_id>\d+)/$', views.info, name="info"),
    url(r'^challenge/(?P<challenge_id>\d+)/edit/$', views.editChallenge, name="edit"),
    url(r'^my/$', views.myChallenges, name="myChallenges"),
    url(r'^create/$', views.createChallenge, name="create"),
    url(r'^user/(?P<user_id>\d+)/$', views.showAccount, name="account"),
    url(r'^editAccount/$', views.editAccount, name="editAccount"),
    url(r'^createAccount/$', views.createAccount, name="createAccount"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'challenges/login.html',
                                                         'current_app': 'challenges'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'challenges:index'}, name="logout"),
    url(r'^changePassword/$', 'django.contrib.auth.views.password_change',
            {'template_name': 'challenges/changePassword.html', 'current_app': 'challenges',
             'post_change_redirect': 'challenges:index'}, name="changePassword"),
)
