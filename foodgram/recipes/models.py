from django.contrib.auth import get_user_model
from django.db import models

from .utils import get_unknown_user

User = get_user_model()


class Ingredient(models.Model):

    title = models.CharField('Название ингредиента', max_length=255)
    dimension = models.CharField('единица измерения', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='amounts',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey('Recipe',
                               on_delete=models.CASCADE,
                               related_name='ingredient_amounts',
                               verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField('Количество')

    def __str__(self):
        return self.ingredient.title


class Tag(models.Model):
    tag = models.CharField(max_length=15, verbose_name='Тэг')
    color = models.CharField(max_length=15, verbose_name='Цвет')
    slug = models.CharField(max_length=15,
                            verbose_name='Название на английском')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.SET(get_unknown_user),
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField('Название', max_length=255)
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Изображение')
    description = models.TextField('Описание', max_length=1000)
    ingredients = models.ManyToManyField(Ingredient,
                                         through=IngredientAmount,
                                         related_name='recipes',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Тэги')
    duration = models.PositiveSmallIntegerField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='users_favorite',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='fav_recipes',
                               verbose_name='Рецепт')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_unique')
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
