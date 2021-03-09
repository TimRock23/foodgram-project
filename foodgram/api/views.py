from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, filters

from .serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        title = self.request.query_params.get('query', None)
        if title is not None:
            queryset = queryset.filter(title__startswith=title)
            return queryset
