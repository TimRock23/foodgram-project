from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from foodgram.settings import TAGS

from .models import Ingredient, IngredientAmount, Recipe, Tag


def get_ingredients(request):
    """Достать ингредиенты и их количество при создании рецепта"""
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value]
    return ingredients


def save_ingredients(ingredients, recipe):
    """Сохранить ингредиенты рецепта в БД"""
    if recipe.ingredients.exists():
        IngredientAmount.objects.filter(recipe=recipe).delete()

    for key in ingredients:
        IngredientAmount.objects.create(
            amount=ingredients[key],
            ingredient=get_object_or_404(Ingredient, title=key),
            recipe=recipe,
        )


def get_purchase_recipes_from_session(session):
    """Получить список рецептов, добавленных в список покупок"""
    recipes_ids = session.get('recipe_ids')
    if recipes_ids is not None:
        recipes = Recipe.objects.filter(pk__in=recipes_ids)
        return recipes


def create_shop_list(session):
    """Создать текстовый файл со списком покупок и отправить пользователю"""
    recipes = get_purchase_recipes_from_session(session)
    ingredients = recipes.values(
        'ingredients__title',
        'ingredients__dimension').annotate(
            total_amount=Sum('ingredient_amounts__amount')
    )
    filename = 'shopping_list.txt'
    content = ''
    for ingredient in ingredients:
        string = (f'{ingredient["ingredients__title"]} '
                  f'({ingredient["ingredients__dimension"]}) — '
                  f'{ingredient["total_amount"]}')
        content += string + '\n'
    response = HttpResponse(content=content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def get_active_tags(request):
    """Получить список активных тегов для фильтрации рецептов"""
    tags = set()
    if 'tags' in request.GET:
        tags = set(request.GET.getlist('tags'))
        tags.intersection_update(set(TAGS))
    return tags


def filter_by_tags(recipes, tags):
    """Отфильтровать рецепты по тегам"""
    return recipes.filter(tags__slug__in=tags).distinct()


def get_context(request, recipes_list):
    """Создание контекста для генерации страниц"""
    tags_active = get_active_tags(request)
    if tags_active:
        recipes_list = filter_by_tags(recipes_list, tags_active)
    paginator = Paginator(recipes_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    context = {'page': page,
               'tags': tags,
               'paginator': paginator,
               'tags_active': tags_active}
    return context
