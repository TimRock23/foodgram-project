from django import template

from users.models import Follow


register = template.Library()


@register.filter()
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter()
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


@register.filter()
def is_subscribed(author, user):
    return Follow.objects.filter(user=user, author=author).exists()