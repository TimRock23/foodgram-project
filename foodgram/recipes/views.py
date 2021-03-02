from django.shortcuts import get_object_or_404, render, redirect, \
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import Recipe, Tag


def index(request):
    recipes_list = Recipe.objects.order_by('-pub_date').all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator,
                                          'tags': tags})


def new_recipe(request):
    pass