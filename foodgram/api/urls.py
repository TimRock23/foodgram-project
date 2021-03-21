from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'ingredients',
                views.IngredientsViewSet,
                basename='ingredients')
router.register(r'subscriptions',
                views.SubscriptionsViewSet,
                basename='subscriptions')
router.register(r'favorites',
                views.FavoritesViewSet,
                basename='favorites')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/purchases/', views.add_recipe_to_purchase),
    path('v1/purchases/<int:id>/', views.delete_recipe_from_purchase_api),
]
