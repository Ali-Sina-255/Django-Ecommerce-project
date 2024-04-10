from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.store, name='store'),
    path('<category_slug>/', views.store, name='product_by_category'),
]