from django.contrib import admin

from .models import Ingredient, Recipe, IngredientCount, Tag, Favorite


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'dimension')
    search_fields = ('name',)
    list_filter = ('dimension',)
    empty_value_display = '-пусто-'


class IngredientCountInline(admin.TabularInline):
    model = IngredientCount


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'duration',)
    search_fields = ('author', 'name',)
    list_filter = ('tag',)
    empty_value_display = '-пусто-'
    inlines = (IngredientCountInline,)


class IngredientCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'count')
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'color')
    search_fields = ('tag',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientCount, IngredientCountAdmin)
admin.site.register(Favorite, FavoriteAdmin)
