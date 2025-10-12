from django.urls import path

from . import views

app_name = 'Task_Manager'

urlpatterns = [
    path('', views.home, name='home')
]