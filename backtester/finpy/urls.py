from django.conf.urls import patterns, url
from finpy import views

urlpatterns = patterns( "",
        url(r'^$', views.index, name='index'),
        url(r'^plotter/', views.plotter, name='plot'),

)
