from django.forms import CheckboxSelectMultiple, ModelForm, Textarea
from django.shortcuts import render

from .models import Recipe
from .services import get_ingredients, save_ingredients


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'duration', 'description', 'image')
        widgets = {
            'tags': CheckboxSelectMultiple(),
            'description': Textarea(attrs={'rows': '8'}),
        }

    def save_recipe(self, request):
        """Сохранить рецепт в БД"""
        recipe = self.save(commit=False)
        recipe.author = request.user
        ingredients = get_ingredients(request)

        if len(ingredients) == 0:
            return render(request, 'new_recipe.html', {'form': self})

        recipe.save()
        save_ingredients(ingredients, recipe)
        self.save_m2m()
