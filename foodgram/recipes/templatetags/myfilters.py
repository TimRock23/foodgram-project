from django import template

from recipes.models import Favorite
from users.models import Follow

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def count_format(word, count):
    exceptions = [11, 12, 13, 14]
    count -= 3
    remainder_by_10 = count % 10
    remainder_by_100 = count % 100
    if remainder_by_10 == 1 and remainder_by_100 != 11:
        return word + ''
    elif remainder_by_10 < 5 and remainder_by_100 not in exceptions:
        return word + 'а'
    else:
        return word + 'ов'


@register.filter
def is_subscribed(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def in_favorites(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def purchase_size(request):
    recipe_ids = request.session.get('recipe_ids')
    if recipe_ids is None:
        return 0
    else:
        return len(recipe_ids)


@register.simple_tag
def activate_tag(current_url, tag):
    if '?' in current_url:
        return f'{current_url}&tags={tag}'
    return f'{current_url}?tags={tag}'


@register.simple_tag
def deactivate_tag(request, tags=None, param=''):
    tags = list(tags)
    tags.remove(param)
    params = '&'.join(f'tags={tag}' for tag in tags)
    if 'page' in request.GET:
        path = str(request.get_full_path())
        params_with_page = path.split('&')
        if len(params) > 0:
            return f'{params_with_page[0]}&{params}'
        else:
            return f'{params_with_page[0]}'
    return f'?{params}'
