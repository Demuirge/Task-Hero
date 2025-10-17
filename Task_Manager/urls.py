from django.urls import path

from . import views

app_name = 'Task_Manager'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/<int:task_id>/', views.task, name='task'),
    path('create-task/', views.create_task, name='create_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('confirm-delete-task/<int:task_id>/', views.confirm_delete_task, name='confirm_delete_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/complete/', views.mark_task_completed, name='mark_task_completed'),
]