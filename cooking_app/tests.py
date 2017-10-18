from django.test import TestCase
from cooking_app.models import Category, Recipe, Article


class CategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("run setUpTestData (Category=>embeddedCategory)...: TestDrink=>TestCoctail")
        Category.objects.create(name="TestDrink")
        drink = Category.objects.get(name="TestDrink")
        Category.objects.create(name="TestCoctail",
                                parent=drink)
        Recipe.objects.create(name="TestRecipe",
                              recipe="TestTextRecipe",
                              category=drink)
        Article.objects.create(name="TestArticle",
                               about="AboutArticle",
                               article="TextArticle",
                               category=drink)

    def testRootCategory(self):
        print("run testRootCategory ...")
        drink = Category.objects.get(name="TestDrink").is_root_node()
        self.assertTrue(drink)

    def testChildCategory(self):
        print("run testChildCategory ...")
        coctail = Category.objects.get(name="TestCoctail").is_child_node()
        self.assertTrue(coctail)

    def testCategoryChange(self):
        print("run testRecipeChange ...")
        category = Category.objects.get(name="TestCoctail")
        category.name = "NewCategory"
        category.save()
        self.assertEquals(category.name, "NewCategory")

    def testCategoryDelete(self):
        print("run testCategoryDelete ...")
        Category.objects.get(name="TestDrink").delete()
        try:
            category = Recipe.objects.get(name="TestRecipe")
            self.assertFalse(category)
        except:
            category = False
            self.assertFalse(category)

    def testRecipeGet(self):
        print("run testRecipeGet ...")
        recipe = Recipe.objects.get(name="TestRecipe")
        self.assertEquals(recipe.name, "TestRecipe")

    def testRecipeChange(self):
        print("run testRecipeChange ...")
        recipe = Recipe.objects.get(name="TestRecipe")
        recipe.name = "NewRecipe"
        recipe.save()
        self.assertEquals(recipe.name, "NewRecipe")

    def testRecipeDelete(self):
        print("run testCategoryDelete ...")
        Recipe.objects.get(name="TestRecipe").delete()
        try:
            recipe = Recipe.objects.get(name="TestRecipe")
            self.assertFalse(recipe)
        except:
            recipe = False
            self.assertFalse(recipe)

    def testArticleGet(self):
        print("run testArticleGet ...")
        article = Article.objects.get(name="TestArticle")
        self.assertEquals(article.name, "TestArticle")

    def testArticleChange(self):
        print("run testArticleChange ...")
        article = Article.objects.get(name="TestArticle")
        article.name = "NewArticle"
        article.save()
        self.assertEquals(article.name, "NewArticle")

    def testArticleDelete(self):
        print("run testArticleDelete ...")
        Article.objects.get(name="TestArticle").delete()
        try:
            article = Article.objects.get(name="TestArticle")
            self.assertFalse(article)
        except:
            article = False
            self.assertFalse(article)
