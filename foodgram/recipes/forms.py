from django.forms import ModelForm, CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tag', 'ingredients', 'duration', 'description',
                  'photo', 'slug')
        widgets = {
            'tags': CheckboxSelectMultiple()
        }
        help_texts = {
            'name': 'Название блюда',
            'photo': 'Выберите фото',
            'description': 'Описание',
            'ingredients': 'Выберите ингредиенты',
            'tag': 'Выберите теги',
            'duration': 'Время приготовления в минутах',
            'slug': 'Короткая ссылка на рецепт(на английском)'
        }