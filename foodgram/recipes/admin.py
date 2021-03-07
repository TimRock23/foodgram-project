from django.contrib import admin

from .models import Ingredient, Recipe, IngredientCount, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'dimension')
    search_fields = ('name',)
    list_filter = ('dimension',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'duration',)
    search_fields = ('author', 'name',)
    list_filter = ('tag',)
    empty_value_display = '-пусто-'


class IngredientCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'count')
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'color')
    search_fields = ('tag',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientCount, IngredientCountAdmin)
