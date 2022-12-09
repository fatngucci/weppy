from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.snack_list, name='snack-list'),
    path('show/<int:pk>/', views.snack_detail, name='snack-detail'),
    path('comment/<int:pk>/vote/<str:up_or_down>/', views.vote, name='comment-vote'),
    path('show/<int:pk>/delete', views.snack_delete, name='snack-delete'),
    path('add/', views.snack_create, name='snack-create'),
    path('search/', views.snack_search, name='snack-search'),
]