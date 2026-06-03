# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('microsoft-login/', views.microsoft_login, name='microsoft_login'),
#     path('auth/callback/', views.auth_callback, name='auth_callback'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('logout/', views.logout_view, name='logout'),
#     # path('dashboard/', views.dashboard, name='dashboard'),
#     # path('copies/', views.copies_list, name='copies_list'),
#     # path('copies/<int:email_id>/', views.copy_detail, name='copy_detail'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.login_view,        name='login'),
    path('microsoft-login/',  views.microsoft_login,   name='microsoft_login'), path('auth/callback/',    views.auth_callback,     name='auth_callback'),
    path('dashboard/',        views.dashboard_view,    name='dashboard'),
    path('logout/',           views.logout_view,       name='logout'),
    path('files/',            views.file_list,         name='file_list'),
    path('files/upload/',     views.upload_file,       name='upload_file'),
    path('files/share/<int:pk>/',  views.share_file,   name='share_file'),
    path('files/delete/<int:pk>/', views.delete_file,  name='delete_file'),
]