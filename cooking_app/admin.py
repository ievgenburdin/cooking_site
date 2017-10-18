from django.contrib import admin
# MPTT using for nesting categories, read on https://django-mptt.readthedocs.io/
from mptt.admin import MPTTModelAdmin,DraggableMPTTAdmin
from cooking_app.models import Category, Recipe, Article
"""
class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_admin_ident = 30
    #mptt_indent_field = "some_node_field"
"""


class CategoryAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'article', 'category')
    prepopulated_fields = {'slug': ('name',)}


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'category')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin,
                    list_display=(
                        'tree_actions',
                        'indented_title',
                    ),
                    list_display_links=(
                        'indented_title',
                        ),
                    )


