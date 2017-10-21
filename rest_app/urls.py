from django.conf.urls import url
from rest_app import views


urlpatterns = [
    url(r'^categories/$', views.get_category_by_id, name='get_category_by_id'),
]