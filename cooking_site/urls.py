"""cooking_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cooking_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.show_home_page, name='show_home_page'),
    url(r'^categories/$', views.show_categories, name='show_categories'),
    url(r'^category/show/(?P<category_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/create/$', views.create_category, name='create_category'),
    url(r'^category/change/(?P<category_slug>[\w\-]+)/$', views.change_category, name='change_category'),
    url(r'^category/delete/$', views.delete_category, name='delete_category'),
    url(r'^recipes/$', views.show_recipes, name='show_recipes'),
    url(r'^recipe/create/$', views.create_recipe, name='create_recipe'),
    url(r'^recipe/show/(?P<recipe_slug>[\w\-]+)/$', views.show_recipe, name='show_recipe'),
    url(r'^recipe/change/(?P<recipe_slug>[\w\-]+)/$', views.change_recipe, name='change_recipe'),
    url(r'^recipes/delete/$', views.delete_recipe, name='delete_recipe'),
    url(r'^articles/$', views.show_articles, name='show_articles'),
    url(r'^article/show/(?P<article_slug>[\w\-]+)/$', views.show_article, name='show_article'),
    url(r'^article/create/$', views.create_article, name='create_article'),
    url(r'^article/change/(?P<article_slug>[\w\-]+)/$', views.change_article, name='change_article'),
    url(r'^article/delete/$', views.delete_article, name='delete_article'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
