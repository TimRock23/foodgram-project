from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/new', views.new_recipe, name='new_recipe')
]
