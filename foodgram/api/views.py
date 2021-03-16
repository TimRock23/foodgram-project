from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import  View
from django.http import JsonResponse

from .serializers import (IngredientSerializer, FollowSerializer,
                          FavoriteSerializer)

from recipes.models import Ingredient, Favorite
from users.models import User, Follow


class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': True})


class IngredientsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        title = self.request.query_params.get('query', None)
        if title is not None:
            queryset = queryset.filter(title__startswith=title)
            return queryset


class SubscriptionsViewSet(CreateDeleteViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_object(self):
        queryset = self.get_queryset()
        author_id = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset,
                                user=self.request.user,
                                author__id=author_id)
        return obj

    # def perform_create(self, serializer):
    #     following = get_object_or_404(User, id=self.request.data['id'])
    #     if self.request.user != following:
    #         Follow.objects.get_or_create(user=self.request.user,
    #                                      author=following)


class FavoritesViewSet(CreateDeleteViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_object(self):
        queryset = self.get_queryset()
        recipe_id = self.kwargs.get(self.lookup_field)
        obj = get_object_or_404(queryset,
                                user=self.request.user,
                                recipe__id=recipe_id)
        return obj

