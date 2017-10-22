from django.http import HttpResponse
from cooking_app.models import Category, Recipe, Article
from django.core.exceptions import ObjectDoesNotExist
import json


def category(request):
    if request.method == "GET":
        category_slug = request.GET['category_slug']
        try:
            category = Category.objects.get(slug=category_slug)
            category_tree = category.get_ancestors(ascending=True, include_self=True)
            category_list = []
            for parent in category_tree:
                category_object = {
                    'name': parent.name,
                    'slug': parent.slug}
                category_list.append(category_object)
            response_data = {
                'name': category.name,
                'slug': category.slug,
                'parents_list': category_list}
        except ObjectDoesNotExist:
            response_data = {'errors': "Object does not exist"}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    else:
        return HttpResponse(status=404)


def get_content(request):
    if request.method == "GET":
        slug = request.GET['slug']
        response_data = {}
        try:
            article = Article.objects.get(slug=slug)
            response_data['article'] = {'name': article.name,
                                        'about': article.about,
                                        'article': article.article,
                                        'category': article.category.name}
        except ObjectDoesNotExist:
            response_data['article'] = {'errors': "Article does not exist"}
        try:
            recipe = Recipe.objects.get(slug=slug)
            response_data['recipe'] = {'name': recipe.name,
                                       'recipe': recipe.recipe,
                                       'category': recipe.category.name}
        except ObjectDoesNotExist:
            response_data['recipe'] = {'errors': "Recipe does not exist"}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")


def get_categories(request):
    if request.method == "GET":
        slug = request.GET['slug']
        response_data = {}
        try:
            article = Article.objects.get(slug=slug)
            article_category_tree = article.category.get_ancestors(ascending=True,
                                                                   include_self=True)
            article_category_list = []
            for parent in article_category_tree:
                category_object = {'name': parent.name}
                article_category_list.append(category_object)
            response_data['article'] = {'name': article.name,
                                        'categories': article_category_list}
        except ObjectDoesNotExist:
            response_data['article'] = {'errors': "Article does not exist"}
        try:
            recipe = Recipe.objects.get(slug=slug)
            recipe_category_tree = recipe.category.get_ancestors(ascending=True,
                                                                 include_self=True)
            recipe_category_list = []
            for parent in recipe_category_tree:
                category_object = {'name': parent.name}
                recipe_category_list.append(category_object)
            response_data['recipe'] = {'name': recipe.name,
                                       'categories': recipe_category_list}
        except ObjectDoesNotExist:
            response_data['recipe'] = {'errors': "Recipe does not exist"}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")


def category_content(request):
    if request.method == "GET":
        category_slug = request.GET['slug']
        response_data = {}
        try:
            category = Category.objects.get(slug=category_slug)
            response_data['category_name'] = category.name
            try:
                recipes = Recipe.objects.filter(category=category)
                recipe_list = []
                for recipe_object in recipes:
                    recipe_list.append({'name': recipe_object.name,
                                        'recipe': recipe_object.recipe})
                response_data['recipes'] = recipe_list
            except ObjectDoesNotExist:
                response_data['recipes'] = {'errors': "Recipe does not exits"}
            try:
                articles = Article.objects.filter(category=category)
                article_list = []
                for article_object in articles:
                    article_list.append({'name': article_object.name,
                                         'about': article_object.about,
                                         'article': article_object.article})
                response_data['article'] = article_list
            except ObjectDoesNotExist:
                response_data['article'] = {'errors': "Article does not exist"}
        except ObjectDoesNotExist:
            response_data['errors'] = "Category does not exist"
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
