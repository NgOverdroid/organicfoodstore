from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name ='home'),
    path('search/', views.search, name='search'),
    path('fruits/', views.fruits, name='fruits'),
    path('meat/', views.meat, name='meat'),
    path('vegetables/', views.vegetables, name='vegetables'),
    path('seafood/', views.seafood, name='seafood'),
    path('carbs/', views.carbs, name='carbs'),
    path('about/', views.about, name="about"),
    path('product/<int:pk>', views.product, name='product')
]