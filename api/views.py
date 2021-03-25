from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient
from users.models import Follow

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer)


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
        title = self.request.query_params.get('query')
        if title is None:
            return Response(data={'success': False},
                            status=status.HTTP_404_NOT_FOUND)

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


@api_view(['POST'])
def add_recipe_to_purchase(request):
    recipe_id = request.data.get('id')
    if recipe_id is None:
        return Response(data={'success': False},
                        status=status.HTTP_400_BAD_REQUEST)
    recipe_id = int(recipe_id)
    recipes = request.session.get('recipe_ids')
    if not recipes:
        recipes = []
    recipes.append(recipe_id)
    request.session['recipe_ids'] = recipes
    return Response(data={'success': True},
                    status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_recipe_from_purchase_api(request, id):
    try:
        recipes = request.session['recipe_ids']
    except KeyError:
        return Response(data={'success': False},
                        status=status.HTTP_404_NOT_FOUND)
    if id not in recipes:
        return Response(data={'success': False},
                        status=status.HTTP_404_NOT_FOUND)
    recipes.remove(id)
    request.session['recipe_ids'] = recipes
    return Response(data={'success': True},
                    status=status.HTTP_200_OK)
