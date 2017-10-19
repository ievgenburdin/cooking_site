from django import forms
from django.core.exceptions import ObjectDoesNotExist
from cooking_app.models import Category, Recipe, Article


class CategoryForm:
    def _init__(self, name, parent_name):
        self.name = name
        self.parent_name = parent_name
        self.errors = " "

    def length_is_valid(self):
        if 0 < len(self.name) <= 50:
            valid = True
        else:
            valid = False
            self.errors = "Name is too long or empty"
        return valid

    def unique_is_valid(self):
        try:
            Category.objects.get(name=self.name)
            self.errors = "This name already exist"
            return False
        except ObjectDoesNotExist:
            return True

    def parent_is_valid(self):
        if self.parent_name == "":
            valid = True
        else:
            try:
                Category.objects.get(name=self.parent_name)
                valid = True
            except ObjectDoesNotExist:
                valid = False
                self.errors = "Parent does not exist"
        return valid

class RecipeForm:
    def _init__(self, name, parent_name, recipe):
        self.name = name
        self.parent_name = parent_name
        self.recipe = recipe
        self.errors = " "

    def length_is_valid(self):
        if 0 < len(self.name) <= 50:
            if 0 < len(self.recipe) <= 1000:
                valid = True
            else:
                self.errors = "Recipe field is too long or empty"
                valid = False
        else:
            self.errors = "Name is too long or empty"
            valid = False
        return valid

    def unique_is_valid(self):
        try:
            Recipe.objects.get(name=self.name)
            valid = False
            self.errors = "Recipe with same name already exist"
        except ObjectDoesNotExist:
            valid = True
        return valid

    def category_is_valid(self):
        try:
            Category.objects.get(name=self.parent_name)
            valid = True
        except ObjectDoesNotExist:
            print("Category does not exist")
            self.errors = "Category does not exist"
            valid = False
        return valid


class ArticleForm:
    def _init__(self, name, parent_name, about, article):
        self.name = name
        self.parent_name = parent_name
        self.about = about
        self.article = article
        self.errors = " "

    def length_is_valid(self):
        if 0 < len(self.name) <= 50:
            if 0 < len(self.article) <= 1000:
                if 0 < len(self.about) <= 100:
                    valid = True
                else:
                    self.errors = "About field is too long or empty"
                    valid = False
            else:
                self.errors = "Article field is too long or empty"
                valid = False
        else:
            self.errors = "Name is too long or empty"
            valid = False
        return valid

    def unique_is_valid(self):
        try:
            Article.objects.get(name=self.name)
            valid = False
            self.errors = "Article with same name already exist"
        except ObjectDoesNotExist:
            valid = True
        return valid

    def category_is_valid(self):
        try:
            Category.objects.get(name=self.parent_name)
            valid = True
        except ObjectDoesNotExist:
            print("Category does not exist")
            self.errors = "Category does not exist"
            valid = False
        return valid
