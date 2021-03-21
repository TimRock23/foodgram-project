from django.contrib import admin

from .models import Favorite, Ingredient, IngredientAmount, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'duration', 'count_of_favs')
    search_fields = ('author', 'name', 'name',)
    list_filter = ('author', 'tags',)
    empty_value_display = '-пусто-'
    inlines = (IngredientAmountInline,)

    def count_of_favs(self, obj):
        return obj.fav_recipes.count()


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'recipe')
    search_fields = ('ingredient', 'recipe')
    list_filter = ('recipe',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'color')
    search_fields = ('tag',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user',)
