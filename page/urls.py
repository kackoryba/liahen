from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    #uvodne kecy, kontakt, demo, faq,...
    url(r'^', include('about.urls', namespace="about")), 
    #zadania, riesenia uloh; sady
    url(r'^tasks/', include('tasks.urls', namespace="tasks")),
    #submity, statistiky
    url(r'^submits/', include('submit.urls', namespace="submit")),

    #django admin
    url(r'^admin/', include(admin.site.urls)),
    #login
    url(r'^account/', include('ksp_login.urls')),    
]
