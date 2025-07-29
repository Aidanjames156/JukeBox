from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_albums, name='search_albums'),
    path('results/', views.search_results, name='search_results'),
]
