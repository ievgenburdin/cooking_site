from django.conf.urls import url
from rest_app import views


urlpatterns = [
    url(r'^category/$', views.category, name='category'),
    url(r'^get_content/$', views.get_content, name='get_content'),
    url(r'^get_categories/$', views.get_categories, name='get_categories'),
    url(r'^category_content/$', views.category_content, name='category_content')
]
