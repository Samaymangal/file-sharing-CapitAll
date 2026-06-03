from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('microsoft-login/', views.microsoft_login, name='microsoft_login'),
    path('auth/callback/', views.auth_callback, name='auth_callback'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]