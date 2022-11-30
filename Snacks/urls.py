from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.snacks_list, name='snack-list'),
    path('show/<int:pk>/', views.snacks_detail, name='snack-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='snack-vote'),
    path('show/<int:pk>/delete', views.snacks_delete, name='snack-delete'),
    path('add/', views.snacks_create, name='snack-create'),
]