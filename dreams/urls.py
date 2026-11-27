from django.urls import path
from . import views


urlpatterns = [
    path('dreams/', views.dream_list, name='dream_list'),
    path('dreams/create/', views.dream_create, name='dream_create'),
    path('dreams/<int:pk>/edit/', views.dream_update, name='dream_update'),
    path('dreams/<int:pk>/delete/', views.dream_delete, name='dream_delete'),
]