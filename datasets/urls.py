from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datasets/', views.datasets, name='datasets'),
    path('dataset/<int:dataset_id>/', views.dataset, name='dataset'),
    path('scrape/<int:dataset_id>/', views.scrape_dataset, name='scrape_dataset'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]
