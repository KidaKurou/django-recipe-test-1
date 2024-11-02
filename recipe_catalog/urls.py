from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('about/', views.about, name='about'),
]