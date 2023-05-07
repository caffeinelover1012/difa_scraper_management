from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datasets/', views.datasets, name='datasets'),
    path('dataset/<int:dataset_id>/', views.dataset, name='dataset'),
    path('dataset/<int:dataset_id>/modification_request/', views.create_modification_request, name='create_modification_request'),
    path('scrape/<int:dataset_id>/', views.scrape_dataset, name='scrape_dataset'),
    path('collections/', views.collections, name='collections'),
    path('collections/<int:collection_id>/', views.collection, name='collection'), 
    path('collections/create/', views.create_collection, name='create_collection'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('modification_requests/', views.modification_requests, name='modification_requests'),
    path('modification_requests/view_changes/<int:mod_request_id>/', views.view_changes, name='view_changes'),
    path('modification_requests/approve/<int:mod_request_id>/', views.approve_request, name='approve_request'),
    path('modification_requests/reject/<int:mod_request_id>/', views.reject_request, name='reject_request'),
    path('modification_requests/modify/<int:mod_request_id>/', views.modify_modification_request, name='modify_modification_request'),
    path('modification_requests/delete/<int:mod_request_id>/', views.delete_modification_request, name='delete_modification_request'),
    path('export_dataset/<int:dataset_id>/', views.export_dataset, name='export_dataset'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('research_team/', views.research_team, name='research_team'),
    path('leadership_team/', views.leadership_team, name='leadership_team'),
    path('search/', views.searchpage, name='search'),
    path('logout/', views.user_logout, name='logout'),
]
