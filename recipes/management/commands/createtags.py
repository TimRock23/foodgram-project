from collections import namedtuple

from django.core.management.base import BaseCommand

from recipes.models import Tag

Tags_tuple = namedtuple('Tag', ['tag', 'color', 'slug'])

br = Tags_tuple(tag='Завтрак', color='orange', slug='breakfast')
ln = Tags_tuple(tag='Обед', color='green', slug='lunch')
dn = Tags_tuple(tag='Ужин', color='purple', slug='dinner')

tags = [br, ln, dn]


class Command(BaseCommand):
    help = 'Creat 3 base tags: Breakfast, Lunch, Dinner'

    def handle(self, *args, **options):
        for tag in tags:
            if Tag.objects.filter(slug=tag.slug).exists():
                print(f'{tag.slug} already exist')
            else:
                Tag.objects.create(tag=tag.tag, slug=tag.slug, color=tag.color)
                print(f'{tag.slug} instance created')
