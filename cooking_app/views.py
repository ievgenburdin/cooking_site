from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cooking_app.models import Category, Recipe, Article
from cooking_app.forms import CategoryForm, RecipeForm, ArticleForm
from django.core.exceptions import ObjectDoesNotExist


def show_home_page(request):
    categories = Category.objects.all()
    num_categories = len(categories)
    recipes = Recipe.objects.all()
    num_recipes = len(recipes)
    articles = Article.objects.all()
    num_articles = len(articles)
    return render(request, 'cooking_app/home.html', {'num_categories': num_categories,
                                                     'num_recipes': num_recipes,
                                                     'num_articles': num_articles,
                                                     'page': 'home'
                                                     })


def show_categories(request):
    category_list = Category.objects.all()
    return render(request,
                  'cooking_app/category/categories.html',
                  {'categories': category_list,
                   'page': 'categories'})


def show_category(request, category_slug ):
    try:
        category = Category.objects.get(slug=category_slug)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    try:
        articles = Article.objects.filter(category=category)
    except ObjectDoesNotExist:
        articles=[]
    try:
        recipes = Recipe.objects.filter(category=category)
    except ObjectDoesNotExist:
        recipes=[]
    categories = category.get_ancestors(ascending=False, include_self=True)
    return render(request,
                  'cooking_app/category/show_category.html',
                  {'category': category,
                   'categories': categories,
                   'articles': articles,
                   'recipes': recipes,
                   'page': 'categories'
                   })


def create_category(request):
    if request.method == "POST":
        new_category = CategoryForm()
        new_category.name = request.POST['name']
        new_category.parent_name = request.POST['parent']
        if new_category.length_is_valid() and\
                new_category.unique_is_valid() and\
                new_category.parent_is_valid():
            if new_category.parent_name == "":
                Category.objects.create(name=new_category.name)
            else:
                parent = Category.objects.get(name=new_category.parent_name)
                Category.objects.create(name=new_category.name, parent=parent)
            return HttpResponseRedirect('/categories/')
        else:
            print(new_category.errors)
            categories = Category.objects.all()
            return render(request,
                          'cooking_app/category/create_category.html',
                          {'categories': categories,
                           'errors': new_category.errors})
    else:
        categories = Category.objects.all()
        return render(request,
                      'cooking_app/category/create_category.html',
                      {'categories': categories,
                       'page': 'categories'})


def change_category(request, category_slug):
    if request.method == "POST":
        new_category = CategoryForm()
        new_category.name = request.POST['name']
        new_category.parent_name = request.POST['parent']
        if new_category.length_is_valid() and \
                new_category.parent_is_valid():
            category = Category.objects.get(slug=category_slug)
            category.name = new_category.name
            if new_category.parent_name == "":
                category.parent = None
            else:
                category.parent = Category.objects.get(name=new_category.parent_name)
            category.save()
            return HttpResponseRedirect('/categories/')
        else:
            print(new_category.errors)
            category = Category.objects.get(slug=category_slug)
            categories = Category.objects.all()
            return render(request,
                          'cooking_app/category/change_category.html',
                          {'categories': categories,
                           'category': category,
                           'errors': new_category.errors,
                           'page': 'categories'})
    else:
        category = Category.objects.get(slug=category_slug)
        categories = Category.objects.all()
        return render(request,
                      'cooking_app/category/change_category.html',
                      {'categories': categories,
                       'category': category,
                       'page': 'categories'})


def delete_category(request):
    if request.method == "POST":
        category_slug = request.POST["category_slug"]
        try:
            Category.objects.get(slug=category_slug).delete()
        except ObjectDoesNotExist:
            print("Object does not exist")
            return HttpResponse("Object does not exist")
        return HttpResponseRedirect('/categories/')
    return HttpResponse(status=404)


def show_recipes(request):
    recipe_list = Recipe.objects.all()
    return render(request,
                  'cooking_app/recipe/recipes.html',
                  {'recipes': recipe_list,
                   'page': 'recipes'})


def show_recipe(request, recipe_slug):
    recipe = Recipe.objects.get(slug=recipe_slug)
    categories = recipe.category.get_ancestors(ascending=False, include_self=True)
    return render(request,
                  'cooking_app/recipe/show_recipe.html',
                  {'categories': categories,
                   'recipe': recipe,
                   'page': 'recipes'})


def create_recipe(request):
    if request.method == "POST":
        new_recipe = RecipeForm()
        new_recipe.name = request.POST['name']
        new_recipe.parent_name = request.POST['category']
        new_recipe.recipe = request.POST['recipe']
        if new_recipe.length_is_valid() and\
                new_recipe.unique_is_valid() and\
                new_recipe.category_is_valid():
            Recipe.objects.create(name=new_recipe.name,
                                  category=Category.objects.get(name=new_recipe.parent_name),
                                  recipe=new_recipe.recipe)

            return HttpResponseRedirect('/recipes/')
        else:
            categories = Category.objects.all()
            return render(request,
                          'cooking_app/recipe/create_recipe.html',
                          {'categories': categories,
                           'errors': new_recipe.errors,
                           'page': 'recipes'})
    else:
        categories = Category.objects.all()
        return render(request,
                      'cooking_app/recipe/create_recipe.html',
                      {'categories': categories,
                       'page': 'recipes'})


def change_recipe(request, recipe_slug):
    if request.method == "POST":
        new_recipe = RecipeForm()
        new_recipe.name = request.POST['name']
        new_recipe.parent_name = request.POST['category']
        new_recipe.recipe = request.POST['recipe']
        if new_recipe.length_is_valid() and new_recipe.category_is_valid():
            recipe = Recipe.objects.get(slug=recipe_slug)
            recipe.name = new_recipe.name
            recipe.category = Category.objects.get(name=new_recipe.parent_name)
            recipe.recipe = new_recipe.recipe
            recipe.save()
            return HttpResponseRedirect('/recipes/')
        else:
            recipe = Recipe.objects.get(slug=recipe_slug)
            categories = Category.objects.all()
            return render(request,
                          'cooking_app/recipe/change_recipe.html',
                          {'categories': categories,
                           'recipe': recipe,
                           'errors': new_recipe.errors,
                           'page': 'recipes'})
    else:
        recipe = Recipe.objects.get(slug=recipe_slug)
        categories = Category.objects.all()
        return render(request,
                      'cooking_app/recipe/change_recipe.html',
                      {'categories': categories,
                       'recipe': recipe,
                       'page': 'recipes'})


def delete_recipe(request):
    if request.method == "POST":
        recipe_slug = request.POST["recipe_slug"]
        try:
            Recipe.objects.get(slug=recipe_slug).delete()
        except ObjectDoesNotExist:
            print("Object does not exist")
            return HttpResponse("Object does not exist")
        return HttpResponseRedirect('/recipes/')
    return HttpResponse(status=404)


def show_articles(request):
    article_list = Article.objects.all()
    return render(request,
                  'cooking_app/articles/articles.html',
                  {'articles': article_list,
                   'page': 'articles'})


def show_article(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    categories = article.category.get_ancestors(ascending=False, include_self=True)
    return render(request,
                  'cooking_app/articles/show_article.html',
                  {'categories': categories,
                   'article': article,
                   'page': 'articles'})


def create_article(request):
    if request.method == "POST":
        new_article = ArticleForm()
        new_article.name = request.POST['name']
        new_article.parent_name = request.POST['category']
        new_article.about = request.POST['about']
        new_article.article = request.POST['article']
        if new_article.length_is_valid() and\
                new_article.unique_is_valid() and\
                new_article.category_is_valid():
            Article.objects.create(name=new_article.name,
                                   category=Category.objects.get(name=new_article.parent_name),
                                   about=new_article.about,
                                   article=new_article.article)
            return HttpResponseRedirect('/articles/')
        else:
            categories = Category.objects.all()
            return render(request,
                          'cooking_app/articles/create_article.html',
                          {'categories': categories,
                           'errors': new_article.errors,
                           'page': 'articles'})
    else:
        categories = Category.objects.all()
        return render(request,
                      'cooking_app/articles/create_article.html',
                      {'categories': categories,
                       'page': 'articles'})


def change_article(request, article_slug):
    if request.method == "POST":
        new_article = ArticleForm()
        new_article.name = request.POST['name']
        new_article.parent_name = request.POST['category']
        new_article.about = request.POST['about']
        new_article.article = request.POST['article']
        if new_article.length_is_valid() and \
                new_article.category_is_valid():
            article = Article.objects.get(slug=article_slug)
            article.name = new_article.name
            article.category = Category.objects.get(name=new_article.parent_name)
            article.about = new_article.about
            article.recipe = new_article.article
            article.save()
            return HttpResponseRedirect('/articles/')
        else:
            article = Article.objects.get(slug=article_slug)
            categories = Category.objects.all()
            return render(request,
                          'cooking_app/articles/change_article.html',
                          {'categories': categories,
                           'article': article,
                           'errors': new_article.errors,
                           'page': 'articles'})
    else:
        article = Article.objects.get(slug=article_slug)
        categories = Category.objects.all()
        return render(request,
                      'cooking_app/articles/change_article.html',
                      {'categories': categories,
                       'article': article,
                       'page': 'articles'})


def delete_article(request):
    if request.method == "POST":
        article_slug = request.POST["article_slug"]
        try:
            Article.objects.get(slug=article_slug).delete()
        except ObjectDoesNotExist:
            print("Object does not exist")
            return HttpResponse("Object does not exist")
        return HttpResponseRedirect('/articles/')
    return HttpResponse(status=404)

