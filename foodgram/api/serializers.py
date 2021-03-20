from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from recipes.models import Ingredient, Favorite, Recipe
from users.models import User, Follow


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Ingredient


class FollowSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=User.objects.all(),
                          slug_field='id',
                          source='author')

    class Meta:
        fields = ('id',)
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=Recipe.objects.all(),
                          slug_field='id',
                          source='recipe')

    class Meta:
        fields = ('id',)
        model = Favorite
