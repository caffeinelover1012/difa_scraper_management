from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, CleanedDatasetViewSet
router = DefaultRouter()
router.register(r'datasets/clean', CleanedDatasetViewSet)
router.register(r'datasets', DatasetViewSet)

urlpatterns = [
    path('', views.searchpage, name='index'),
    path('api/', include(router.urls)),
    path('search/', views.searchpage, name='search'),
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
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('research_team/', views.research_team, name='research_team'),
    path('leadership_team/', views.leadership_team, name='leadership_team'),
    path('scrape_all/', views.scrape_all_view, name = 'scrape_all'),
    path('workshop/', views.workshop, name = 'workshop'),
    path('partners/', views.partners, name='partners'),
    path('scrape_progress/', views.scraping_progress_view, name = 'scrape_progress'),
    path('search-results/', views.search_results, name='search_results'),
    path('logout/', views.user_logout, name='logout'),
]
