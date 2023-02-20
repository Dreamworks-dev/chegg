from django.urls import path
from . import views


app_name = 'scrape_engine'
urlpatterns = [
    path('', views.main, name='index'),
    path('result', views.result, name='result'),
]
