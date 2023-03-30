from django.urls import path
from . import views

app_name = 'datasets'

urlpatterns = [
    path('', views.index, name='index'),
    # Add more URL patterns here
]
