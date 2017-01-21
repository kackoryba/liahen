from django.conf.urls import url

from about import views

urlpatterns = [
    #home page Liahne
    url(r'^$', views.intro_view, name = 'intro'),
]