from django.urls import path
from . import views

urlpatterns = [
    #path('delete/', views.snack_delete_view, name='snack-delete-cs'),
    path('edit/<int:pk>/', views.snack_edit_view, name='snack-edit'),
    path('', views.snack_manage_view, name='snack-manage')
    #path('editdelete/<int:pk>/', views.comment_edit_delete, name='comment-edit-delete'),
]