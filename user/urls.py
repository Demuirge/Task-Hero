from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('log-in/', auth_views.LoginView.as_view(template_name = "user/log_in.html"), name= 'log_in'),
    path('log-out/', auth_views.LogoutView.as_view(), name= 'log_out'),
]