from django.shortcuts import get_object_or_404, render, redirect, \
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import Recipe, Tag
from .forms import RecipeForm


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
    tags = Tag.objects.all()
    if request.method != 'POST':
        form = RecipeForm
        return render(request, 'new_recipe.html', {'form': form,
                                                   'tags': tags})

    form = RecipeForm(request.POST, files=request.FILES)
    if form.is_valid():
        recipe_new = form.save(commit=False)
        recipe_new.author = request.user
        recipe_new.save()
        return redirect('index')

    return render(request, 'new_recipe.html', {'form': form,
                                               'tags': tags})
