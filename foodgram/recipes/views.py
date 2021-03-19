from django.shortcuts import get_object_or_404, render, redirect, \
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings


from users.models import Follow
from .models import Recipe, Tag, IngredientAmount, Ingredient, User, Favorite
from .forms import RecipeForm
from . import services


def index(request):
    recipes_list = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipes_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    purchase_count = services.get_purchase_count_from_session(
        request.session)
    title = 'Рецепты'
    return render(request, 'index.html', {'page': page,
                                          'tags': tags,
                                          'title': title,
                                          'paginator': paginator,
                                          'purchase_count': purchase_count})


@login_required()
def new_recipe(request):
    if request.method != 'POST':
        form = RecipeForm
        return render(request, 'new_recipe.html', {'form': form})

    form = RecipeForm(request.POST, files=request.FILES)
    if form.is_valid():
        services.save_recipe(request, form)
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
        services.save_recipe(request, form)
        return redirect('index')

    return render(request, 'new_recipe.html', {'recipe': recipe, 'form': form})


@login_required
def recipe_delete(request, username, recipe_id):
    user = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, author=user, id=recipe_id)

    if request.user != user:
        return redirect('recipe_id',
                        username=recipe.author.username,
                        recipe_id=recipe_id)

    recipe.delete()
    return redirect('index')


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.recipes.order_by('-pub_date').all()
    paginator = Paginator(recipes_list, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    title = author.get_full_name()
    return render(request, 'index.html', {'page': page,
                                          'tags': tags,
                                          'title': title,
                                          'author': author,
                                          'paginator': paginator})


@login_required
def follow_page(request):
    following_authors = request.user.follower.all()
    paginator = Paginator(following_authors, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'page': page,
                                             'paginator': paginator})


@login_required
def favorite_page(request):
    favorite_recipes = Recipe.objects.filter(fav_recipes__user=request.user)
    paginator = Paginator(favorite_recipes, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    title = 'Избранное'
    return render(request, 'index.html', {'tags': tags,
                                          'page': page,
                                          'title': title,
                                          'paginator': paginator})


def purchase_page(request):
    recipes = services.get_purchase_recipes_from_session(request.session)
    is_empty = False
    if len(recipes) == 0:
        is_empty = True
    return render(request, 'shopList.html', {'recipes': recipes,
                                             'is_empty': is_empty})


def del_recipe_from_purchase(request, recipe_id):
    try:
        recipes = request.session['recipe_ids']
    except KeyError:
        return redirect('purchase')
    if recipe_id not in recipes:
        return redirect('purchase')
    recipes.remove(recipe_id)
    request.session['recipe_ids'] = recipes
    return redirect('purchase')


def download_shop_list(request):
    shop_list = services.create_shop_list(request.session)
    return shop_list

# recipe = get_object_or_404(Recipe, pk=recipe_id)
# ingredients = IngredientAmount.objects.filter(recipe=recipe).all()
# for ingredient in ingredients:
#     title = ingredient.ingredient.title
#     dimension = ingredient.ingredient.dimension
#     amount = ingredient.amount
