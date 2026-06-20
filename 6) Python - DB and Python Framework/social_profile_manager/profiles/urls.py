"""
Section C - Task 4: Clean URL Routing

Each view gets its own clearly-named path, and every URL has a `name=`
so templates and redirect() calls never need to hardcode raw paths
(e.g. {% url 'profile_list' %} instead of "/profiles/").
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('create/', views.profile_create, name='profile_create'),
    path('<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('export/', views.profile_export_csv, name='profile_export_csv'),
]
