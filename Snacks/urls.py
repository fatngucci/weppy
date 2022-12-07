from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.snacks_list, name='snack-list'),
    path('show/<int:pk>/', views.snacks_detail, name='snack-detail'),
    path('comment/<int:pk>/vote/<str:up_or_down>/', views.vote, name='comment-vote'),
    path('show/<int:pk>/delete', views.snacks_delete, name='snack-delete'),
    path('add/', views.snacks_create, name='snack-create'),
    path('search/', views.snack_search, name='snack-search'),
]