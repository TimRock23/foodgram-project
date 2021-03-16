from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, SubscriptionsViewSet, FavoritesViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'subscriptions',
                SubscriptionsViewSet,
                basename='subscriptions')
router.register(r'favorites', FavoritesViewSet, basename='favorites')


urlpatterns = [
    path('', include(router.urls)),
    # path('subscriptions/', SubscriptionView.as_view()),
    # path('subscriptions/<int:author_id>/', SubscriptionView.as_view()),
]
