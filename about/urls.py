from django.conf.urls import url

from about import views


urlpatterns = [
    # home page Liahne
    url(r'^$', views.intro_view, name='intro'),
    url(r'^about$', views.about_view, name='about'),
    url(r'^contact$', views.contact_view, name='contact'),
    url(r'^terms$', views.terms_view, name='terms'),
]
