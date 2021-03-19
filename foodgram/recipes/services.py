from django.shortcuts import get_object_or_404, render, redirect, \
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

from django.db.models import Sum
from django.http import HttpResponse

from users.models import Follow
from .models import Recipe, Tag, IngredientAmount, Ingredient, User, Favorite
from .forms import RecipeForm


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


def get_purchase_count_from_session(session):
    recipe_ids = session.get('recipe_ids')
    if recipe_ids is None:
        return 0
    else:
        return len(recipe_ids)


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


# ingredients = IngredientCount.objects.filter(recipe=recipe).all()
# for ingredient in ingredients:
#     title = ingredient.ingredient.title
#     dimension = ingredient.ingredient.dimension
#     count = ingredient.count

