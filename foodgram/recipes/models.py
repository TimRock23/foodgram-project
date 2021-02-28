from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def get_unknown_user():
    return User.objects.get_or_create(username='unknown')[0]


class Ingredient(models.Model):
    name = models.CharField('ingredient', max_length=255)
    dimension = models.CharField('unit of measurement', max_length=255)

    def __str__(self):
        return self.name


class IngredientCount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='count',
                                   verbose_name='ingredient')
    count = models.FloatField(verbose_name='count')

    def __str__(self):
        return self.ingredient.name


class Tag(models.Model):

    # class TagChoice(models.TextChoices):
    #     BREAKFAST = 'br', _('Завтрак')
    #     LUNCH = 'ln', _('Обед')
    #     DINNER = 'dn', _('Ужин')
    #
    # tag = models.CharField(max_length=7, choices=TagChoice.choices,
    #                        verbose_name='tag')

    tag = models.CharField(max_length=15, verbose_name='tag')
    color = models.CharField(max_length=15, verbose_name='color')

    def __str__(self):
        return self.tag


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_unknown_user),
                               related_name='recipes',
                               verbose_name='author')
    name = models.CharField('recipe', max_length=255)
    photo = models.ImageField(upload_to='recipes/')
    description = models.TextField('description', max_length=1000)
    ingredients = models.ManyToManyField(IngredientCount,
                                         related_name='recipes',
                                         verbose_name='ingredient')
    tag = models.ManyToManyField(Tag, related_name='recipes',
                                 verbose_name='tag')
    duration = models.PositiveSmallIntegerField('cooking time')
    pub_date = models.DateTimeField('publication time', auto_now_add=True)
    slug = models.SlugField('slug', blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
