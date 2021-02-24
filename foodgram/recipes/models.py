from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def get_unknown_user():
    return User.objects.get_or_create(username='unknown')[0]


class Ingredient(models.Model):
    name = models.CharField('ingredient', max_length=255)
    measurement = models.CharField('unit of measurement', max_length=255)


class IngredientCount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='count')
    count = models.FloatField()


class Tag(models.Model):
    tag = models.CharField(max_length=63)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_unknown_user),
                               related_name='recipes')
    name = models.CharField('recipe', max_length=255)
    description = models.TextField('description', max_length=1000)
    ingredients = models.ManyToManyField(IngredientCount,
                                         related_name='recipes')
    tag = models.ManyToManyField(Tag, related_name='recipes')
    duration = models.PositiveSmallIntegerField('cooking time')
    slug = models.SlugField('slug', blank=True, null=True, unique=True)
