from django.urls import path
from . import views

# app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('resat_password_validate/<uidb64>/<token>/', views.resat_password_validate, name='resat_password_validate'),
    path('resat_password/', views.resat_password, name='resat_password')
]
