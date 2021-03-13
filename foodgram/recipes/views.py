from django.shortcuts import get_object_or_404, render, redirect, \
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from users.models import Follow
from .models import Recipe, Tag, IngredientCount, Ingredient, User
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
        IngredientCount.objects.filter(recipe=recipe).delete()

    for key in ingredients:
        IngredientCount.objects.create(
            count=ingredients[key],
            ingredient=Ingredient.objects.get(title=key),
            recipe=recipe,
        )


def index(request):
    recipes_list = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator,
                                          'tags': tags})


@login_required()
def new_recipe(request):
    if request.method != 'POST':
        form = RecipeForm
        return render(request, 'new_recipe.html', {'form': form})

    form = RecipeForm(request.POST, files=request.FILES)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        ingredients = get_ingredients(request)

        if len(ingredients) == 0:
            return render(request, 'new_recipe.html', {'form': form})

        recipe.save()
        save_ingredients(ingredients, recipe)
        form.save_m2m()
        return redirect('index')

    return render(request, 'new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author=user, id=recipe_id)

    if request.user != user:
        return redirect('recipe_id',
                        username=recipe.author.username,
                        recipe_id=recipe_id)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)

    if form.is_valid():
        recipe_changed = form.save(commit=False)
        ingredients = get_ingredients(request)

        if len(ingredients) == 0:
            return render(request, 'new_recipe.html', {'form': form})

        recipe_changed.save()
        save_ingredients(ingredients, recipe_changed)
        form.save_m2m()
        return redirect('index')

    return render(request, 'new_recipe.html', {'recipe': recipe, 'form': form})


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.recipes.order_by('-pub_date').all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, 'profile.html', {'page': page,
                                            'author': author,
                                            'paginator': paginator,
                                            'tags': tags})


@login_required
def follow_page(request):
    following_authors = request.user.follower.all()
    paginator = Paginator(following_authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page,
                                             'paginator': paginator})
