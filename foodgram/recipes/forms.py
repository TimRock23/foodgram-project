from django.forms import ModelForm, CheckboxSelectMultiple, Textarea

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tag', 'duration', 'description', 'image')
        widgets = {
            'tag': CheckboxSelectMultiple(),
            'description': Textarea(attrs={'rows': '8'}),
        }
