from django.conf.urls import url
from . import views
print "****************************app urls.py"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^pokes$', views.pokes, name='pokes'),
    url(r'^login$', views.login, name='login'),
    url(r'^poke/(?P<user_id>\d+)$', views.poke, name = "poke"),
]