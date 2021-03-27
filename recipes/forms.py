from django.forms import CheckboxSelectMultiple, ModelForm, Textarea

from .models import Recipe
from .services import save_ingredients


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'duration', 'description', 'image')
        widgets = {
            'tags': CheckboxSelectMultiple(),
            'description': Textarea(attrs={'rows': '8'}),
        }

    def save_recipe(self, request, ingredients):
        """Сохранить рецепт в БД"""
        recipe = self.save(commit=False)
        recipe.author = request.user

        recipe.save()
        save_ingredients(ingredients, recipe)
        self.save_m2m()
