from django.conf.urls import url

from submit import views

urlpatterns = [
    #submits/protocol/2/ (detaily submitu)
    url(r'^protocol/(?P<pk>\d+)/$', views.protocol_view, name = 'protocol'),

    #submits/update
    url(r'^update/$', views.update_submit),
    
    #submits/   (vsetky moje)
    url(r'^$', views.judge_view, {'type':'me'}, name = 'index'),   
    #submits/now    (teraz na testovaci)
    url(r'^now/$', views.judge_view, {'type':'now'}, name = 'now'),    
    #submits/task/popolvar   (vsetky uspesne v ulohe)
    url(r'^task/(?P<task>\w+)/$', views.judge_view, {'type':'task'}, name='task'),

    #admin vidi aj:
    #submits/user/fero  (vsetky user-ove)
    url(r'^user/(?P<user>\w+)/$', views.judge_view, {'type':'user'}, name='user'),
    #submits/user/fero/task/popolvar    (vsetky user-ove v ulohe)
    url(r'^user/(?P<user>\w+)/task/(?P<task>\w+)/$', views.judge_view, {'type':'user_task'}, name='user_task'),
]


''' 
    #V buducnosti: statistiky
    #submits/users
    url(r'^users/$', views.users_view, name = 'users'),    
    #submits/tasks
    url(r'^tasks/$', views.index_view, name = 'tasks'),   
    #submits/schools
    url(r'^schools/$', views.index_view, name = 'schools'),    
)
'''
