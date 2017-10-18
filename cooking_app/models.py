from django.db import models
# MPTT using for nesting categories, read on https://django-mptt.readthedocs.io/
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.core.exceptions import ObjectDoesNotExist


class Category(MPTTModel):
    name = models.CharField(max_length=50,
                            unique=True)
    parent = TreeForeignKey('self',
                            blank=True,
                            null=True,
                            related_name='children',
                            db_index=True,
                            on_delete=models.CASCADE)
    slug = models.SlugField(blank=True,
                            unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name


class AbstractContent(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    slug = models.SlugField(blank=True,
                            unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Recipe(AbstractContent):
    recipe = models.TextField(max_length=1000,
                              blank=False,
                              default="Here must be a recipe text")

    class Meta:
        verbose_name_plural = "Recipes"
        verbose_name = "Recipe"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        try:
            Recipe.objects.get(slug=self.slug)
            self.slug += '-1'
        except ObjectDoesNotExist:
            pass
        finally:
            super(Recipe, self).save(*args, **kwargs)


class Article(AbstractContent):
    about = models.TextField(max_length=100,
                             blank=False,
                             default="Here must be few word about article")
    article = models.TextField(max_length=1000,
                               blank=False,
                               default="Here must be article content")

    class Meta:
        verbose_name_plural = "Articles"
        verbose_name = "Article"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        try:
            Article.objects.get(slug=self.slug)
            self.slug += "-1"
        except ObjectDoesNotExist:
            pass
        finally:
            super(Article, self).save(*args, **kwargs)
