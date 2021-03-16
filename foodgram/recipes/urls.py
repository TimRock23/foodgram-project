from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('follow/', views.follow_page, name='follow_page'),
    path('favorites/', views.favorite_page, name='favorites'),
    path('recipe/new', views.new_recipe, name='new_recipe'),
    path('<str:username>/<int:recipe_id>/',
         views.recipe_view,
         name='recipe_id'),
    path('<str:username>/<int:recipe_id>/edit/',
         views.recipe_edit,
         name='recipe_edit'),
    path('<str:username>/profile/', views.profile, name='profile'),
]
