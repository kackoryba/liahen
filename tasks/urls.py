from django.conf.urls import url

from tasks import views
from tasks.models import TaskSet, Task, Stalker

urlpatterns = [
    #tasks/    (aktualna sada usera)
    url(r'^$', views.task_set_graph_view, name = 'index'),
    #tasks/set/intro  (konkretna sada ako list)
    url(r'^set/(?P<pk>\w+)$', views.task_set_view, name = 'set'),
    #tasks/set/intro/graph    (konkretna sada ako graf)
    url(r'^set/(?P<pk>\w+)/graph$', views.task_set_graph_view, name = 'set_graph'),
    #tasks/popolvar   (zadanie ulohy/studijny text)
    url(r'^(?P<pk>\w+)$', views.task_view, name='task'),
    #tasks/popolvar/ex-sol    (vzorove riesenie ulohy)
    url(r'^(?P<pk>\w+)/ex-sol$', views.example_solution_view, name='example_solution'),
]