from django.urls import path
from . import views

urlpatterns = [
    # path('delete/', views.snack_delete_view, name='snack-delete-cs'),
    path('edit/snack/<int:pk>/', views.snack_edit_view, name='snack-edit'),
    path('manage/snack/', views.snack_manage_view, name='snack-manage'),
    path('edit/comment/<int:pk>/', views.comment_edit_view, name='comment-edit-cs'),
    path('manage/comment/', views.comment_manage_view, name='comment-manage'),
    path('', views.menu_view, name='menu')
    # path('editdelete/<int:pk>/', views.comment_edit_delete, name='comment-edit-delete'),
]
