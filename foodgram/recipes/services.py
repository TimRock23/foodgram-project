from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render

from foodgram.settings import TAGS

from .models import Ingredient, IngredientAmount, Recipe, Tag


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value]
    return ingredients


def save_ingredients(ingredients, recipe):
    if recipe.ingredients.exists():
        IngredientAmount.objects.filter(recipe=recipe).delete()

    for key in ingredients:
        IngredientAmount.objects.create(
            amount=ingredients[key],
            ingredient=Ingredient.objects.get(title=key),
            recipe=recipe,
        )


def save_recipe(request, form):
    recipe = form.save(commit=False)
    recipe.author = request.user
    ingredients = get_ingredients(request)

    if len(ingredients) == 0:
        return render(request, 'new_recipe.html', {'form': form})

    recipe.save()
    save_ingredients(ingredients, recipe)
    form.save_m2m()


def get_purchase_recipes_from_session(session):
    recipes_ids = session.get('recipe_ids')
    recipes = Recipe.objects.filter(pk__in=recipes_ids)
    return recipes


def create_shop_list(session):
    recipes = get_purchase_recipes_from_session(session)
    ingredients = recipes.values(
        'ingredients__title',
        'ingredients__dimension').annotate(
            total_amount=Sum('ingredient_amount__amount')
    )
    filename = 'shopping_list.txt'
    content = ''
    for ingredient in ingredients:
        string = f'{ingredient["ingredients__title"]} ' \
                 f'({ingredient["ingredients__dimension"]}) — ' \
                 f'{ingredient["total_amount"]}'
        content += string + '\n'
    response = HttpResponse(content=content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def get_active_tags(request):
    tags = set()
    if 'tags' in request.GET:
        tags = set(request.GET.getlist('tags'))
        tags.intersection_update(set(TAGS))
    return tags


def filter_by_tags(recipes, tags):
    return recipes.filter(tag__slug__in=tags).distinct()


def get_context(request, recipes_list):
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
