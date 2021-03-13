from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, SubscriptionsViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'subscriptions',
                SubscriptionsViewSet,
                basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
    # path('subscriptions/', SubscriptionView.as_view()),
    # path('subscriptions/<int:author_id>/', SubscriptionView.as_view()),
]
